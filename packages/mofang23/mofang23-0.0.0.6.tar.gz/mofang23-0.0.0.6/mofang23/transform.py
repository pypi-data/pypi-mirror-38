# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sfstool
   Description :
   Author :        Asdil
   date：          2018/11/16
-------------------------------------------------
   Change Activity:
                   2018/11/16:
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import pandas as pd
from Asdil import tool
from Asdil import log


class Vcf:
    def __init__(self, panel_path, sfs_save_path=None, sps_save_path=None, skiprows=None, log_path=None):
        """
        :param panel_path:      snpsort文件
        :param sfs_save_path:   sfs保存文件夹
        :param sps_save_path:   sps保存文件夹
        :param skiprows:        vcf #CHROM 在第几行
        """
        assert os.path.exists(panel_path)
        panel = pd.read_table(panel_path)

        self.panel_ref = panel.iloc[:, 2].tolist()
        self.panel_lat = panel.iloc[:, 3].tolist()

        panel = panel.iloc[:, :2]
        panel.columns = ['#CHROM', 'POS']
        self.panel = panel

        self.sfs_save_path = sfs_save_path
        self.sps_save_path = sps_save_path

        if self.sfs_save_path is not None:
            tool.createDir(self.sfs_save_path)

        if self.sps_save_path is not None:
            tool.createDir(self.sps_save_path)
        self.skiprows = None
        if skiprows is not None:
            self.skiprows = int(skiprows)

        self.log = False
        self.log_path = log_path
        if log_path is not None:
            self.log = True
            log.alter_log_ini(self.log_path)

    def read_vcf(self, vcf_path):
        """
        :param vcf_path:  vcf路径
        :return:
        """
        flag = True
        # 去掉vcf注释行
        if self.skiprows is None:
            skiprows = 0
            flag = False
            with open(vcf_path, 'r') as f:
                for line in f:
                    if line[:6] == '#CHROM':
                        flag = True
                        break
                    skiprows += 1
            self.skiprows = skiprows
            assert flag
        assert isinstance(self.skiprows, int)
        vcf = pd.read_table(vcf_path, skiprows=self.skiprows)
        return vcf

    def create_sfs(self, barcode, ref, lat):
        """
        :param barcode: 样本1|1 0|1 列表
        :param ref:     vcf ref列
        :param lat:     vcf lat列
        :return:
        """
        assert len(barcode) == len(ref) == len(lat)
        ret = ''
        for i in range(len(barcode)):
            if barcode[i] == '-':
                ret += '-|-\n'
            elif barcode[i] == '0|0':
                assert ref[i] != '-'
                ret += ref[i] + '|' + ref[i] + '\n'

            elif barcode[i] == '1|1':
                assert lat[i] != '-'
                ret += lat[i] + '|' + lat[i] + '\n'

            elif barcode[i] == '0|1':
                assert lat[i] != '-' and ref[i] != '-'
                ret += ref[i] + '|' + lat[i] + '\n'

            elif barcode[i] == '1|0':
                assert lat[i] != '-' and ref[i] != '-'
                ret += lat[i] + '|' + ref[i] + '\n'
            else:
                assert 1 == 2
        return ret[:-1]

    def create_sps(self, sfs):
        ret = ''
        for i in range(len(sfs)):
            if sfs[i] == '-|-':
                ret += '.'
            else:
                haplotype1, haplotype2 = sfs[i].split('|')
                if haplotype1 == haplotype2:
                    if haplotype1 == self.panel_ref[i]:
                        ret += '0'
                    elif haplotype1 == self.panel_lat[i]:
                        ret += '2'
                    else:
                        ret += '.'
                else:
                    if haplotype1 == self.panel_ref[i] or haplotype1 == self.panel_lat[i]:
                        if haplotype2 == self.panel_ref[i] or haplotype2 == self.panel_lat[i]:
                            ret += '1'
                        else:
                            ret += '.'
                    else:
                        ret += '.'
        return ret

    def vcf2sfs(self, vcf_path):
        """
        :param vcf_path: vcf路径
        :return:
        """
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        if not os.path.exists(vcf_path):
            print(f'{vcf_path} 文件不存在')
            if self.log:
                logger.info(f'{vcf_path} 文件不存在')
            return 0

        if self.sfs_save_path is None:
            print('sfs文件保存路径为空')
            if self.log:
                logger.info('sfs文件保存路径为空')
                assert self.sfs_save_path is not None

        print(f'{vcf_path} 开始读取')
        if self.log:
            logger.info(f'{vcf_path} 开始读取')

        vcf = self.read_vcf(vcf_path)
        vcf = pd.merge(self.panel, vcf, how='left', on=['#CHROM', 'POS'])
        vcf = vcf.fillna('-')
        columns = vcf.columns.tolist()
        useless_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']

        ref = vcf['REF'].tolist()
        lat = vcf['ALT'].tolist()
        barcodes = tool.diffSet(columns, useless_columns)
        for barcode in barcodes:
            _barcode = '-'.join(barcode.split('_')[1:4]).split('.')[0]
            save_path = tool.pathJoin(self.sfs_save_path, _barcode) + '.sfs'

            barcode = vcf.loc[:, barcode].tolist()
            sfs = self.create_sfs(barcode, ref, lat)
            with open(save_path, 'w') as f:
                f.write(sfs)
            print(f'{_barcode} sfs已经保存!')
            if self.log:
                logger.info(f'{_barcode} sfs已经保存!')
        print(f'{vcf_path} sfs全部转换完毕')
        if self.log:
            logger.info(f'{vcf_path} sfs全部转换完毕')

    def vcf2sps(self, vcf_path):
        """
        :param vcf_path: vcf路径
        :return:
        """
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        if not os.path.exists(vcf_path):
            print(f'{vcf_path} 文件不存在')
            if self.log:
                logger.info(f'{vcf_path} 文件不存在')
            return 0

        if self.sps_save_path is None:
            print('sps文件保存路径为空')
            if self.log:
                logger.info('sps文件保存路径为空')
            assert self.sps_save_path is not None

        print(f'{vcf_path} 开始读取')
        if self.log:
            logger.info(f'{vcf_path} 开始读取')

        vcf = self.read_vcf(vcf_path)
        vcf = pd.merge(self.panel, vcf, how='left', on=['#CHROM', 'POS'])
        vcf = vcf.fillna('-')
        columns = vcf.columns.tolist()
        useless_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']

        ref = vcf['REF'].tolist()
        lat = vcf['ALT'].tolist()
        barcodes = tool.diffSet(columns, useless_columns)
        for barcode in barcodes:
            _barcode = '-'.join(barcode.split('_')[1:4]).split('.')[0]
            save_path = tool.pathJoin(self.sps_save_path, _barcode) + '.sps'

            barcode = vcf.loc[:, barcode].tolist()
            sfs = self.create_sfs(barcode, ref, lat)
            sfs = sfs.split('\n')
            sps = self.create_sps(sfs)
            with open(save_path, 'w') as f:
                f.write(sps)
            print(f'{_barcode} sps已经保存!')
            if self.log:
                logger.info(f'{_barcode} sps已经保存!')
        print(f'{vcf_path} sps全部转换完毕')
        if self.log:
            logger.info(f'{vcf_path} sps全部转换完毕')

    def sfs2sps(self, sfs_path):
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        if not os.path.exists(sfs_path):
            print(f'{sfs_path} 文件不存在')
            if self.log:
                logger.info(f'{sfs_path} 文件不存在')
            return 0

        with open(sfs_path, 'r') as f:
            sfs = f.read()
        sfs = sfs.split('\n')
        sps = self.create_sps(sfs)
        _, _barcode, _, _ = tool.splitPath(sfs_path)
        save_path = tool.pathJoin(self.sps_save_path, _barcode) + '.sps'
        with open(save_path, 'w') as f:
            f.write(sps)
        print(f'{_barcode} sps已经保存!')
        if self.log:
            logger.info(f'{_barcode} sps已经保存!')

    def vcf2sfs_sps(self, vcf_path):
        """
        :param vcf_path: vcf路径
        :return:
        """
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        if not os.path.exists(vcf_path):
            print(f'{vcf_path} 文件不存在')
            if self.log:
                logger.info(f'{vcf_path} 文件不存在')
            return 0

        if self.sfs_save_path is None:
            print('sfs文件保存路径为空')
            if self.log:
                logger.info('sfs文件保存路径为空')
                assert self.sfs_save_path is not None

        if self.sps_save_path is None:
            print('sps文件保存路径为空')
            if self.log:
                logger.info('sps文件保存路径为空')
            assert self.sps_save_path is not None

        print(f'{vcf_path} 开始读取')
        if self.log:
            logger.info(f'{vcf_path} 开始读取')

        vcf = self.read_vcf(vcf_path)
        vcf = pd.merge(self.panel, vcf, how='left', on=['#CHROM', 'POS'])
        vcf = vcf.fillna('-')
        columns = vcf.columns.tolist()
        useless_columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']

        ref = vcf['REF'].tolist()
        lat = vcf['ALT'].tolist()
        barcodes = tool.diffSet(columns, useless_columns)
        for barcode in barcodes:
            _barcode = '-'.join(barcode.split('_')[1:4]).split('.')[0]

            sfs_save_path = tool.pathJoin(self.sfs_save_path, _barcode) + '.sfs'
            sps_save_path = tool.pathJoin(self.sps_save_path, _barcode) + '.sps'

            barcode = vcf.loc[:, barcode].tolist()
            sfs = self.create_sfs(barcode, ref, lat)
            with open(sfs_save_path, 'w') as f:
                f.write(sfs)
            print(f'{_barcode} sfs已经保存!')
            if self.log:
                logger.info(f'{_barcode} sfs已经保存!')

            sfs = sfs.split('\n')
            sps = self.create_sps(sfs)
            with open(sps_save_path, 'w') as f:
                f.write(sps)
            print(f'{_barcode} sps已经保存!')
            if self.log:
                logger.info(f'{_barcode} sps已经保存!')

        print(f'{vcf_path} sfs和sps全部转换完毕')
        if self.log:
            logger.info(f'{vcf_path} sfs和sps全部转换完毕')