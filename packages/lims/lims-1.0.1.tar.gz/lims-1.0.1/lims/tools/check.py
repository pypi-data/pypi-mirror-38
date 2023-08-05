#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

from lims.tools.login import login
from lims.tools import utils

reload(sys)
sys.setdefaultencoding('utf8')


class Check(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(**kwargs)

    def start(self):

        if not self.kwargs['stage_code']:
            tasks = self.get_approve_task()
            if tasks:
                fields = 'STAGECODE REPORT_TYPE FULLNAME REPORT_NAME REPORT_URL SAMPLECOUNT SUMDATA COMMENTS'.split(
                )
                for n, row in enumerate(tasks, 1):
                    # print row
                    reports = self.get_approve_report(stage_code=row['STAGECODE'])
                    print '\033[36m----- {n}. {STAGECODE} {PROJECTNAME} -----\033[0m'.format(n=n, **row)
                    print '\t'.join(fields)
                    for report in reports:
                        line = '\t'.join(map(lambda x: '{%s}' % x, fields)).format(**report)
                        print line
            else:
                print 'no check task'
            exit(0)

        reports = self.get_approve_report(**self.kwargs)

        if not reports:
            print 'no report to check'
            exit(1)

        if not self.kwargs['report_name']:
            print 'There are {} reports to check:'.format(len(reports))
            for report in reports:
                print '{REPORT_TYPE} {FULLNAME} {REPORT_NAME} {REPORT_URL} {SAMPLECOUNT} {SUMDATA} {COMMENTS}'.format(
                    **report)
        else:
            self.operate_report(reports)

    def get_approve_task(self):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingTask_H&Type=json&p1=Approve'.format(
            **self.kwargs)
        print '>>>[get_approve_task GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        return rows

    def get_approve_report(self, **kwargs):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgReport&Type=json&p1={stage_code}&p2=Approve'.format(
            **dict(self.kwargs, **kwargs))
        print '>>>[get_approve_report GET]', url
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if kwargs.get('report_name'):
            for row in rows:
                if row['REPORT_NAME'] == kwargs.get('report_name'):
                    return row
            return None

        return rows

    def operate_report(self, report):

        print 'dealing with report: {REPORT_GUID} {REPORT_NAME}'.format(**report)
        url = '{base_url}/KF_DataAnalysis.SubmitStaging_H2.lims'.format(**self.kwargs)
        print '>>>[operate_report POST]', url
        payload = [report['REPORT_GUID'], 'Approve', self.kwargs['operation'].title()]
        print payload
        resp = self.session.post(url, json=payload).text

        if resp != '""':
            print 'fail to {operation} the report'.format(**self.kwargs)
            exit(1)

        print '{operation} the report successfully'.format(**self.kwargs)


def parser_add_check(parser):

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code')

    parser.add_argument('-report', '--report-name', help='the report name')

    parser.add_argument(
        '-operation',
        help='the operation to do, choose from (%(choices)s) [default=%(default)s]',
        choices=['submit', 'reject'],
        default='submit')

    parser.set_defaults(func=main)


def main(**args):

    Check(**args).start()


# if __name__ == "__main__":

#     main()
