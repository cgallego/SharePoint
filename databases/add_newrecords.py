# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 09:23:24 2017

@author: Cristina Gallego
"""
import os, os.path
import sys
import string
from sys import argv, stderr, exit
import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker
from mylocalbase import localengine
import localdatabase

class AddNewRecords(object):
    """
    USAGE:
    ============= 
    from add_newrecords import *
    newrecords = AddNewRecords()
    """
    def __init__(self): 
        """ initialize database session """           
        #  create a top level Session configuration which can then be used throughout
        # Create the Session
        self.Session = sessionmaker()
        self.Session.configure(bind=localengine)  # once engine is available
        
    def __call__(self):       
        """ Turn Class into a callable object """
        AddNewRecords() 

    def lesion_2DB(self, findreport):

        [cad_id, anony_dob, mutation, exam_date, accession_no, dicom_no, type_mri,
                 cad_status, lesion_comments, original_report, BIRADS, mass_yn, nonmass_yn, foci_yn] = findreport         
        
        self.session = self.Session() #instantiate a Session
        # Send to database lesion info
        lesion_info = localdatabase.Lesion_record(cad_id, anony_dob, mutation, exam_date, accession_no, dicom_no, type_mri,
                 cad_status, lesion_comments, original_report, BIRADS, mass_yn, nonmass_yn, foci_yn)
        self.session.add(lesion_info)
         
        # Finally send records to database
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            
        return
        
    def radiology_2DB(self, lesion_id, radioinfo):        
        
        [sty_indicator_rout_screening_obsp_yn, sty_indicator_high_risk_yn, sty_indicator_high_risk_brca_1_yn, 
                sty_indicator_high_risk_brca_2_yn, sty_indicator_high_risk_brca_1_or_2_yn, 
                sty_indicator_high_risk_at_yn, sty_indicator_high_risk_other_gene_yn,
                sty_indicator_high_risk_prior_high_risk_marker_yn, sty_indicator_high_risk_prior_personal_can_hist_yn, sty_indicator_high_risk_hist_of_mantle_rad_yn,
                sty_indicator_add_eval_as_folup_yn, sty_indicator_folup_after_pre_exam_yn, 
                sty_indicator_pre_operative_extent_of_dis_yn, sty_indicator_post_operative_margin_yn, sty_indicator_pre_neoadj_trtmnt_yn,
                sty_indicator_prob_solv_diff_img_yn, sty_indicator_scar_vs_recurr_yn, sty_indicator_folup_recommend_yn, 
                sty_indicator_prior_2_prophy_mast_yn] = radioinfo
        
        self.session = self.Session() #instantiate a Session
        # Send to database lesion info
        rad_records = localdatabase.Radiology_record(lesion_id, 
                sty_indicator_rout_screening_obsp_yn, sty_indicator_high_risk_yn, sty_indicator_high_risk_brca_1_yn, 
                sty_indicator_high_risk_brca_2_yn, sty_indicator_high_risk_brca_1_or_2_yn, 
                sty_indicator_high_risk_at_yn, sty_indicator_high_risk_other_gene_yn,
                sty_indicator_high_risk_prior_high_risk_marker_yn, sty_indicator_high_risk_prior_personal_can_hist_yn, sty_indicator_high_risk_hist_of_mantle_rad_yn,
                sty_indicator_add_eval_as_folup_yn, sty_indicator_folup_after_pre_exam_yn, 
                sty_indicator_pre_operative_extent_of_dis_yn, sty_indicator_post_operative_margin_yn, sty_indicator_pre_neoadj_trtmnt_yn,
                sty_indicator_prob_solv_diff_img_yn, sty_indicator_scar_vs_recurr_yn, sty_indicator_folup_recommend_yn, 
                sty_indicator_prior_2_prophy_mast_yn)
                        
        self.session.add(rad_records)
        
        # Finally send records to database
        try:
            self.session.commit()  
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            
        return
        
        
    def gtpathology_2DB(self, lesion_id, gtpathology):        
        
        [pt_procedure_id, proc_dt_datetime, proc_side_int,
                 proc_source_int, proc_guid_int, proc_tp_int, original_report_txt, pt_path_id, histop_core_biopsy_benign_yn, histop_other_txt,
                 histop_benign_bst_parenchyma_yn, histop_tp_isc_ductal_yn, histop_tp_isc_other_txt, in_situ_nucl_grade_int,
                 histop_tp_ic_yn, histop_tp_ic_other_txt, histop_other_2_txt] = gtpathology
        
        self.session = self.Session() #instantiate a Session
        # Send to database lesion info
        gtpatho_records = localdatabase.gtPathology_record(lesion_id, pt_procedure_id, proc_dt_datetime, proc_side_int,
                 proc_source_int, proc_guid_int, proc_tp_int, original_report_txt, pt_path_id, histop_core_biopsy_benign_yn, histop_other_txt,
                 histop_benign_bst_parenchyma_yn, histop_tp_isc_ductal_yn, histop_tp_isc_other_txt, in_situ_nucl_grade_int,
                 histop_tp_ic_yn, histop_tp_ic_other_txt, histop_other_2_txt)
                        
        self.session.add(gtpatho_records)
        
        # Finally send records to database
        try:
            self.session.commit()  
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            
        return