#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import json

from lims.tools.login import login
from lims.tools.project import Project
from lims.tools import utils


reload(sys)
sys.setdefaultencoding('utf8')


class Report(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(**kwargs)

        self.project = Project(**kwargs).get_project_list(**kwargs)[0]

        self.report_ftp = 'ftp://172.17.8.208/KFREPORT'

    def start(self):

        if self.kwargs['filename'] and self.kwargs['type']:
            self.upload_report()
        elif self.kwargs['delete']:
            self.delete_report()
        elif not (self.kwargs['filename']  or self.kwargs['type']):
            self.show_report_status()
        elif not self.kwargs['filename']:
            print 'please supply the report file'
        elif not self.kwargs['type']:
            print 'please specific the report type'

    def has_upload_final(self):

        url = '{base_url}/KF_DataAnalysis.HasUploadFinalReport.lims'.format(**self.kwargs)
        print '>>>[has_upload_final POST]', url

        payload = [self.kwargs['stage_code']]

        return self.session.post(url, json=payload).json()

    def upload_report(self):

        payload = [self.kwargs['stage_code'], self.kwargs['type'].upper(), None, self.kwargs['message']]

        if self.kwargs['type'] == 'final':
            if self.has_upload_final():  # False已上传， True未上传
                print '>>>首次上传结题报告sop和产量信息为必填项，后续无需再次填写'
                sop_method = self.get_sops()
                sample_count = self.kwargs.get('sample_count') or raw_input(
                    'please input the sample count:')
                data_size = self.kwargs.get('data_size') or raw_input(
                    'please input the data size:')

                payload += [sop_method, sample_count, data_size]

        # step1: 上传文件
        url = '{base_url}/Runtime_Support.SaveFileFromHTML.lims?ScriptName=QuickIntro.uploadFileProcessingScript'.format(**self.kwargs)
        print '>>>[upload_processing POST]', url
        with utils.safe_open(self.kwargs['filename'], 'rb') as f:
            resp = self.session.post(url, files={'file': f}).json()

        if not resp['success']:
            print 'upload file failed!'
            exit(1)

        # step2: 填写报告
        payload = resp['result'] + payload

        url = '{base_url}/KF_DataAnalysis.UploadReport_H.lims'.format(**self.kwargs)
        print '>>>[upload_report POST]', url
        resp = self.session.post(url, json=payload).json()

        if resp[-1] == 'SUCCESS':
            report_name = resp[0]
            print 'report upload successfully! see result: {report_ftp}/{report_name}'.format(**dict(self.__dict__, **locals()))

            report_guid = self.get_reports(report_name)['REPORT_GUID']
            print report_guid

        # step3: 提交给DoubleCheck
        url = '{base_url}/KF_DataAnalysis.SubmitStaging_H2.lims'.format(**self.kwargs)
        print '>>>[submit_report POST]', url
        payload = [report_guid, 'Draft', 'Submit']
        resp = self.session.post(url, json=payload).text

        if resp == '""':

            print 'submit report to doublechecker "{DOUBLECHECKER}" successfully!'.format(**self.project)
            self.show_report_status(report_guid)

    def get_sops(self):

        product_code = self.project['PRODUCTCODE']

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.DS_TestRelMethod_H&Type=json&p1=&p2={product_code}'.format(
            **dict(self.kwargs, **locals()))
        print '>>>[get_sop_method GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']
        avail_sops = [sop['VALUE'] for sop in rows]
        if self.kwargs['sop_method']:
            if all(sop in avail_sops for sop in self.kwargs['sop_method'].split(',')):
                return self.kwargs['sop_method']

        # print rows
        print 'optional sop methods are as follows:'
        print '#code\tvalue'
        print '\n'.join('{}\t{}'.format(sop['VALUE'], sop['TEXT']) for idx, sop in enumerate(rows))
        while True:
            sops = raw_input('please choose one or more sop code(separate by comma):')
            all_pass = True
            for choice in sops.split(','):
                if choice not in avail_sops:
                    print 'invalid input: {}'.format(choice)
                    all_pass = False
                    break
            if all_pass:
                return sops

    def get_reports(self, report_name=None):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgReport&Type=json&p1={stage_code}&p2=Draft'.format(**self.kwargs)
        print '>>>[get_reports GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if report_name:
            print report_name
            for row in rows:
                if row['REPORT_NAME'] == report_name:
                    return row
            return None

        return rows

    def delete_report(self):

        report = self.get_reports(self.kwargs['delete'])

        if not report:
            print 'no report names {delete}'.format(**self.kwargs)
            exit(1)

        if report['STATUS'] != 'Draft':
            print '[error] the status of report "{delete}" is "{STATUS}", only "Draft" can be deleted'.format(**dict(self.kwargs, **report))
            exit(1)

        url = '{base_url}/Sunway.DeleteRows.lims'.format(**self.kwargs)
        print '>>>[delete_report POST]', url
        payload = [
            'kf_geneticanalysis_report',
            [report['ORIGREC']]
        ]
        print payload
        resp = self.session.post(url, json=payload)

        if resp.text == 'true':
            print '[info] the report "{delete}" has been deleted'.format(**self.kwargs)

    def show_report_status(self, report_guid=None):

        rows = self.get_reports()
        if not rows:
            print 'This stage code has no report uploaded'
        else:
            fields = 'STATUS DISPSTATUS STAGECODE REPORT_NAME ANALYSTPERSON DOUBLECHECKERNAME OPERATIONSMANAGER REPORT_URL'.split()
            print '\t'.join(fields)
            for row in rows:

                if report_guid and row['REPORT_GUID'] != report_guid:
                    continue
                line = '\t'.join(map(lambda x: '{%s}' % x, fields)).format(**dict(self.project, **row))
                print line


def parser_add_report(parser):

    parser.add_argument('filename', help='the report file to upload', nargs='?')

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code', required=True)

    parser.add_argument(
        '-t',
        '--type',
        help='the type of report, choose from [%(choices)s]',
        choices=['qc', 'mapping', 'final'])

    parser.add_argument(
        '-sop', '--sop-method', help='the sop method for the product')

    parser.add_argument('-count', '--sample-count', help='the count of sample')

    parser.add_argument('-data', '--data-size', help='the total data size')

    parser.add_argument('-msg', '--message', help='the message for this report')

    parser.add_argument(
        '-status',
        '--show-status',
        help='show the report status',
        action='store_true')

    parser.add_argument('-d', '--delete', help='the report name to delete')

    parser.set_defaults(func=main)


def main(**args):

    Report(**args).start()


# if __name__ == "__main__":

#     main()
