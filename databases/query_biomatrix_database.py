# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 10:45:23 2017
"""

import sys, os
import string
import datetime
import numpy as np

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from sqlalchemy.sql import join, select

import database_atExam
import database_atlinkPatho
from mylocalbase import biomatrixengine
import pandas as pd

# query object
class Query_biomatrix(object):
    """
    USAGE:
    =============
    query = Query_biomatrix()
    """
    def __call__(self):       
        """ Turn Class into a callable object """
        Query()     
        
    def __init__(self): 
        """ initialize QueryDatabase """
        self.massreport = []
        self.nonmassreport = []
        self.focireport = []
    
    def queryRadiolinfo(self, StudyID, AccessionN=None):
        """
        run : Query by StudyID/AccesionN pair to local folder NO GRAPICAL INTERFACE. default print to output

        Inputs
        ======
        StudyID : (string)    (required) CAD StudyID # (4-digits)
        AccessionN # : (string)  (optional) CAD Accession # (typically)
        Output:
        ======
        """
        # Create the ORMâ€™s â€œhandleâ€ to the database_atExam: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=biomatrixengine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        if AccessionN:
            Radiolinfo = pd.read_sql(select([database_atExam.Cad_record, database_atExam.Exam_record]).\
                            where(database_atExam.Cad_record.cad_pt_no_txt==StudyID).\
                            where(database_atExam.Exam_record.a_number_txt==AccessionN),session.bind)          
        else:                     
            Radiolinfo = pd.read_sql(select([database_atExam.Cad_record, database_atExam.Exam_record]).\
                                where(database_atExam.Cad_record.cad_pt_no_txt==StudyID),session.bind) 
             
        # output query to pandas frame.
        print Radiolinfo
        
        return Radiolinfo
        
        
    def queryExamFindings(self, StudyID, AccessionN):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (string)    (required) CAD StudyID # (4-digits)
        AccessionN # : (string)  (required) CAD Accession # (typically)
        
        Output
        ======
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=biomatrixengine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        datainfo = []; radioinfo =[]; is_mass=[];  is_nonmass=[]; is_foci=[]; 
        # another way to query without the convinience of a dataframe output
        for pt, cad, exam, finding, in session.query(database_atExam.Pt_record, database_atExam.Cad_record, database_atExam.Exam_record, database_atExam.Exam_Finding).\
                     filter(database_atExam.Pt_record.pt_id==database_atExam.Cad_record.pt_id).\
                     filter(database_atExam.Cad_record.pt_id==database_atExam.Exam_record.pt_id).\
                     filter(database_atExam.Exam_record.pt_exam_id==database_atExam.Exam_Finding.pt_exam_id).\
                     filter(database_atExam.Cad_record.cad_pt_no_txt == StudyID).\
                     filter(database_atExam.Exam_record.a_number_txt == AccessionN).all():   
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, pt.anony_dob_datetime, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.exam_img_dicom_txt, exam.exam_tp_mri_int, exam.mri_cad_status_txt, exam.comment_txt, exam.original_report_txt,
              finding.all_birads_scr_int,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn])
          
           radioinfo.append([exam.sty_indicator_rout_screening_obsp_yn, exam.sty_indicator_high_risk_yn, 
                              exam.sty_indicator_high_risk_brca_1_yn, exam.sty_indicator_high_risk_brca_2_yn, 
                              exam.sty_indicator_high_risk_brca_1_or_2_yn, exam.sty_indicator_high_risk_at_yn, 
                              exam.sty_indicator_high_risk_other_gene_yn, exam.sty_indicator_high_risk_prior_high_risk_marker_yn, 
                              exam.sty_indicator_high_risk_prior_personal_can_hist_yn, exam.sty_indicator_high_risk_hist_of_mantle_rad_yn, 
                              exam.sty_indicator_add_eval_as_folup_yn, exam.sty_indicator_folup_after_pre_exam_yn, 
                              exam.sty_indicator_pre_operative_extent_of_dis_yn, exam.sty_indicator_post_operative_margin_yn, 
                              exam.sty_indicator_pre_neoadj_trtmnt_yn, exam.sty_indicator_prob_solv_diff_img_yn, 
                              exam.sty_indicator_scar_vs_recurr_yn, exam.sty_indicator_folup_recommend_yn, 
                              exam.sty_indicator_prior_2_prophy_mast_yn])
             
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               is_mass.append([finding.all_birads_scr_int, finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int, finding.mri_bk_enh_inten_int, finding.mri_o_find_cysts_yn, finding.lesion_mri_start_image_no_int,  finding.lesion_mri_finish_image_no_int])
               # add mass lesion record table
               colLabelsmass = ("finding.all_birads_scr_int","finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int", "finding.mri_bk_enh_inten_int", "finding.mri_o_find_cysts_yn", "finding.start_image_no_int",  "finding.finish_image_no_int")
               self.massreport = pd.DataFrame(data=np.array(is_mass), columns=list(colLabelsmass))
                             
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               is_nonmass.append([finding.all_birads_scr_int, finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int, finding.mri_bk_enh_inten_int, finding.mri_o_find_cysts_yn, finding.lesion_mri_start_image_no_int,  finding.lesion_mri_finish_image_no_int ])
               # add non-mass lesion record table
               colLabelsnonmass = ("finding.all_birads_scr_int","finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int", "finding.mri_bk_enh_inten_int", "finding.mri_o_find_cysts_yn", "finding.start_image_no_int",  "finding.finish_image_no_int")
               self.nonmassreport = pd.DataFrame(data=np.array(is_nonmass), columns=list(colLabelsnonmass))

           # Find if it's mass or non-mass and process
           if (finding.mri_foci_yn):
               is_foci.append([finding.all_birads_scr_int, finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_foci_distr_int, finding.t2_signal_int, finding.mri_bk_enh_inten_int, finding.mri_o_find_cysts_yn, finding.lesion_mri_start_image_no_int,  finding.lesion_mri_finish_image_no_int])
               # add foci lesion record table
               colLabelsfoci = ("finding.all_birads_scr_int","finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_foci_distr_int", "finding.t2_signal_int", "finding.mri_bk_enh_inten_int", "finding.mri_o_find_cysts_yn", "finding.start_image_no_int",  "finding.finish_image_no_int")
               self.focireport = pd.DataFrame(data=np.array(is_foci), columns=list(colLabelsfoci))
                   
        ####### finish finding masses and non-mass or foci
        # add main CAD record        
        colLabels = ("cad.cad_pt_no_txt", "pt.anony_dob_datetime", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt","exam.exam_img_dicom_txt","exam.exam_tp_mri_int","exam.mri_cad_status_txt","exam.comment_txt","exam.original_report", "finding.all_birads_scr_int", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn")
        self.findreport = pd.DataFrame(data=np.array(datainfo), columns=list(colLabels))
        print self.findreport 
        
        colLabels = ("exam.sty_indicator_rout_screening_obsp_yn", "exam.sty_indicator_high_risk_yn", "exam.sty_indicator_high_risk_brca_1_yn", "exam.sty_indicator_high_risk_brca_2_yn", "exam.sty_indicator_high_risk_brca_1_or_2_yn", "exam.sty_indicator_high_risk_at_yn", 
                     "exam.sty_indicator_high_risk_other_gene_yn", "exam.sty_indicator_high_risk_prior_high_risk_marker_yn", "exam.sty_indicator_high_risk_prior_personal_can_hist_yn", "exam.sty_indicator_high_risk_hist_of_mantle_rad_yn", "exam.sty_indicator_add_eval_as_folup_yn", "exam.sty_indicator_folup_after_pre_exam_yn",
                     "exam.sty_indicator_pre_operative_extent_of_dis_yn", "exam.sty_indicator_post_operative_margin_yn",
                     "exam.sty_indicator_pre_neoadj_trtmnt_yn", "exam.sty_indicator_prob_solv_diff_img_yn",
                     "exam.sty_indicator_scar_vs_recurr_yn", "exam.sty_indicator_folup_recommend_yn",
                     "exam.sty_indicator_prior_2_prophy_mast_yn")
                     
        self.radioinfo = pd.DataFrame(data=np.array(radioinfo), columns=list(colLabels))
        print self.radioinfo 
        print self.massreport 
        print self.nonmassreport 
        print self.focireport 

        return self.findreport, self.radioinfo, self.massreport, self.nonmassreport, self.focireport
                

    def queryifProcedure(self, StudyID, AccessionN):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (string)    (required) CAD StudyID # (4-digits)
        AccessionN # : (string)  (required) CAD Accession # (typically)
        
        Output
        ======
        """
        # Create the ORMâ€™s â€œhandleâ€ to the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=biomatrixengine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        gtpathology=[]; dfgtpathology = []; 
        for cad, exam, finding, proc, patho in session.query(database_atExam.Cad_record, database_atExam.Exam_record, database_atExam.Exam_Finding, database_atlinkPatho.Procedure, database_atlinkPatho.Pathology).\
                     filter(database_atExam.Cad_record.pt_id==database_atExam.Exam_record.pt_id).\
                     filter(database_atExam.Exam_record.pt_exam_id==database_atExam.Exam_Finding.pt_exam_id).\
                     filter(database_atExam.Exam_record.pt_id==database_atlinkPatho.Procedure.pt_id).\
                     filter(database_atlinkPatho.Procedure.pt_procedure_id==database_atlinkPatho.Pathology.pt_procedure_id).\
                     filter(database_atExam.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database_atExam.Exam_record.a_number_txt == str(AccessionN)).all():
     
           # print results
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           gtpathology.append([proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt,
                               patho.pt_path_id, patho.histop_core_biopsy_benign_yn, patho.histop_other_txt, patho.histop_benign_bst_parenchyma_yn,
                               patho.histop_tp_isc_ductal_yn, patho.histop_tp_isc_other_txt, patho.in_situ_nucl_grade_int,
                               patho.histop_tp_ic_yn, patho.histop_tp_ic_other_txt, patho.histop_other_2_txt])
           
           gtpathologyLabels = ("proc.pt_procedure_id",  "proc.proc_dt_datetime",  "proc.proc_side_int",  "proc.proc_source_int",  "proc.proc_guid_int",  "proc.proc_tp_int",  "proc.original_report_txt", 
                               "patho.pt_path_id",  "patho.histop_core_biopsy_benign_yn",  "patho.histop_other_txt",  "patho.histop_benign_bst_parenchyma_yn", 
                               "patho.histop_tp_isc_ductal_yn",  "patho.histop_tp_isc_other_txt",  "patho.in_situ_nucl_grade_int", 
                               "patho.histop_tp_ic_yn",  "patho.histop_tp_ic_other_txt",  "patho.histop_other_2_txt")
        
        # finally put everythin in a pd Dataframe
        dfgtpathology = pd.DataFrame(data=np.array(gtpathology), columns=list(gtpathologyLabels))   
           
        print dfgtpathology

        return dfgtpathology
        
        
"""
----------------------------------------------------------------------
@ Copyright (C) Cristina Gallego, University of Toronto, 2017
----------------------------------------------------------------------
"""
            
if __name__ == '__main__':
    ## initialize query
    query = Query_biomatrix()
    
    # query radiology info by CAD StudyID only
    StudyID = '25'.zfill(4)
    Radiolinfo = query.queryRadiolinfo(StudyID)
    print(Radiolinfo)
    
    # notice that you retrieve all radiology records available from 2011 to 2014
    #f that patient if you want to be specific to only  specific MRRI study/exam them pass the accession number of the study:
    AccessionN = '7002835'
    Radiolinfo = query.queryRadiolinfo(StudyID, AccessionN)
    # example print original radiology report for this study
    print(Radiolinfo['original_report_txt'][0])    
    
    # Now query for tabulated exam findings (accession required)
    # this returns query.findreport with lesion info
    findreport, radioinfo, massreport, nonmassreport, focireport = query.queryExamFindings(StudyID, AccessionN)
    
    # query exam finding if procedure 
    # this return query.gtpathology
    gtpathology = query.queryifProcedure(StudyID, AccessionN)
