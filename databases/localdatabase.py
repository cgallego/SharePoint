# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 09:23:24 2017

@author: Cristina Gallego
"""
import sys, os
import string
import datetime
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import PickleType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from mylocalbase import localengine 
Base = declarative_base(localengine)

#  created a Cad_record mapping 
class Lesion_record(Base):
    """Base for Exam_record class using Declarative. for table lesion
    attributes:
        self.lesion_id = lesion_id
        self.cad_pt_no_txt = cad_id
        self.anony_dob_datetime = cad_dob
        ...
    """
    __tablename__ = 'lesion'
    __table_args__ = {'autoload':True}
    lesion_id = Column(Integer, primary_key=True)
    radiology = relationship("Radiology_record", backref=backref('lesion', order_by=lesion_id))
    gtpathology = relationship("gtPathology_record", backref=backref('lesion', order_by=lesion_id))
    # e.g f_dynamic = relationship("Dynamic_features", backref=backref('lesion', order_by=lesion_id))
    # e.g f_morphology = relationship("Morpho_features", backref=backref('lesion', order_by=lesion_id))
    # e.g f_texture = relationship("Texture_features", backref=backref('lesion', order_by=lesion_id))
    # e.g f_stage1 = relationship("Stage1_record", backref=backref('lesion', order_by=lesion_id))
    
    def __init__(self, cad_id, cad_dob, mutation, exam_date, accession_no, dicom_no, type_mri,
                 cad_status, lesion_comments, original_report, BIRADS, mass_yn, nonmass_yn, foci_yn):      
        self.cad_pt_no_txt = cad_id
        self.anony_dob_datetime = cad_dob
        self.latest_mutation = mutation
        self.exam_dt_datetime = exam_date
        self.exam_a_number_txt = accession_no
        self.exam_img_dicom_txt = dicom_no
        self.exam_tp_mri_int = type_mri
        self.exam_mri_cad_status_txt = cad_status
        self.comment_txt = lesion_comments
        self.original_report = original_report
        self.BIRADS = BIRADS
        self.mri_mass_yn = mass_yn
        self.mri_nonmass_yn = nonmass_yn
        self.mri_foci_yn = foci_yn
        
    def __repr__(self):
        return "<Lesion_record(lesion_id='%s', cad_pt='%s', dicom='%s', a_number='%s', exam_date='%s')>" % (self.lesion_id, self.cad_pt_no_txt, self.exam_img_dicom_txt, self.exam_a_number_txt, self.exam_dt_datetime)

        
#  created a Radiology_record mapping 
class Radiology_record(Base):
    """Base for Radiology_record class using Declarative. for table Radiology_record
    attributes:
        self.lesion_id = lesion_id
        self.cad_pt_no_txt = 
        self.latest_mutation = 
        self.exam_dt_datetime
        self.mri_cad_status_txt 
        self.comment_txt
        self.radiology_rpt_generated_yn
        self.original_report_txt
        self.sty_indicator_rout_screening_obsp_yn
        self.sty_indicator_high_risk_yn
        self.sty_indicator_high_risk_brca_1_yn
        self.sty_indicator_high_risk_brca_2_yn
        self.sty_indicator_high_risk_brca_1_or_2_yn
        self.sty_indicator_high_risk_at_yn
        self.sty_indicator_high_risk_other_gene_yn
        self.sty_indicator_high_risk_prior_high_risk_marker_yn
        self.sty_indicator_high_risk_prior_personal_can_hist_yn
        self.sty_indicator_high_risk_hist_of_mantle_rad_yn
        self.sty_indicator_add_eval_as_folup_yn
        self.sty_indicator_folup_after_pre_exam_yn
        self.sty_indicator_pre_operative_extent_of_dis_yn
        self.sty_indicator_post_operative_margin_yn
        self.sty_indicator_pre_neoadj_trtmnt_yn
        self.sty_indicator_prob_solv_diff_img_yn
        self.sty_indicator_scar_vs_recurr_yn
        self.sty_indicator_folup_recommend_yn
        self.sty_indicator_prior_2_prophy_mast_yn
    """
    __tablename__ = 'radiologyInfo'
    __table_args__ = {'autoload':True}
    radio_id = Column(Integer, primary_key=True)
    lesion_id = Column(Integer, ForeignKey('lesion.lesion_id'))
        
    def __init__(self, lesion_id, 
                 sty_indicator_rout_screening_obsp_yn, sty_indicator_high_risk_yn,
                 sty_indicator_high_risk_brca_1_yn, sty_indicator_high_risk_brca_2_yn, sty_indicator_high_risk_brca_1_or_2_yn,
                 sty_indicator_high_risk_at_yn, sty_indicator_high_risk_other_gene_yn, sty_indicator_high_risk_prior_high_risk_marker_yn,
                 sty_indicator_high_risk_prior_personal_can_hist_yn, sty_indicator_high_risk_hist_of_mantle_rad_yn,
                 sty_indicator_add_eval_as_folup_yn, sty_indicator_folup_after_pre_exam_yn,
                 sty_indicator_pre_operative_extent_of_dis_yn, sty_indicator_post_operative_margin_yn, sty_indicator_pre_neoadj_trtmnt_yn,
                 sty_indicator_prob_solv_diff_img_yn, sty_indicator_scar_vs_recurr_yn, sty_indicator_folup_recommend_yn,
                 sty_indicator_prior_2_prophy_mast_yn):
        
        self.lesion_id = lesion_id
        self.sty_indicator_rout_screening_obsp_yn = sty_indicator_rout_screening_obsp_yn
        self.sty_indicator_high_risk_yn = sty_indicator_high_risk_yn
        self.sty_indicator_high_risk_brca_1_yn = sty_indicator_high_risk_brca_1_yn
        self.sty_indicator_high_risk_brca_2_yn = sty_indicator_high_risk_brca_2_yn
        self.sty_indicator_high_risk_brca_1_or_2_yn = sty_indicator_high_risk_brca_1_or_2_yn
        self.sty_indicator_high_risk_at_yn = sty_indicator_high_risk_at_yn
        self.sty_indicator_high_risk_other_gene_yn = sty_indicator_high_risk_other_gene_yn
        self.sty_indicator_high_risk_prior_high_risk_marker_yn = sty_indicator_high_risk_prior_high_risk_marker_yn
        self.sty_indicator_high_risk_prior_personal_can_hist_yn = sty_indicator_high_risk_prior_personal_can_hist_yn
        self.sty_indicator_high_risk_hist_of_mantle_rad_yn = sty_indicator_high_risk_hist_of_mantle_rad_yn
        self.sty_indicator_add_eval_as_folup_yn = sty_indicator_add_eval_as_folup_yn
        self.sty_indicator_folup_after_pre_exam_yn = sty_indicator_folup_after_pre_exam_yn
        self.sty_indicator_pre_operative_extent_of_dis_yn = sty_indicator_pre_operative_extent_of_dis_yn
        self.sty_indicator_post_operative_margin_yn = sty_indicator_post_operative_margin_yn
        self.sty_indicator_pre_neoadj_trtmnt_yn = sty_indicator_pre_neoadj_trtmnt_yn
        self.sty_indicator_prob_solv_diff_img_yn = sty_indicator_prob_solv_diff_img_yn
        self.sty_indicator_scar_vs_recurr_yn = sty_indicator_scar_vs_recurr_yn
        self.sty_indicator_folup_recommend_yn = sty_indicator_folup_recommend_yn
        self.sty_indicator_prior_2_prophy_mast_yn = sty_indicator_prior_2_prophy_mast_yn
        
        
    def __repr__(self):
        return "<Radiology_record(lesion_id='%s', cad_pt_no_txt='%s')>" % (self.lesion_id, self.cad_pt_no_txt)        


#  created a gtPathology_record mapping 
class gtPathology_record(Base):
    """Base for mass_lesion class using Declarative. for table gtPathology_record
    attributes:
        self.lesion_id = lesion_id
        ...
        self.find_mri_nonmass_dist_int = mri_nonmass_dist
        self.find_mri_nonmass_int_enh_int = mri_nonmass_int_enh   
    """
    __tablename__ = 'gtpathology'
    __table_args__ = {'autoload':True}
    gthisto_id = Column(Integer, primary_key=True)
    lesion_id = Column(Integer, ForeignKey('lesion.lesion_id'))
        
    def __init__(self, lesion_id, pt_procedure_id, proc_dt_datetime, proc_side_int,
                 proc_source_int, proc_guid_int, proc_tp_int, original_report_txt, pt_path_id, histop_core_biopsy_benign_yn, histop_other_txt,
                 histop_benign_bst_parenchyma_yn, histop_tp_isc_ductal_yn, histop_tp_isc_other_txt, in_situ_nucl_grade_int,
                 histop_tp_ic_yn, histop_tp_ic_other_txt, histop_other_2_txt):
        self.lesion_id = lesion_id
        self.pt_procedure_id = pt_procedure_id
        self.proc_dt_datetime = proc_dt_datetime
        self.proc_side_int = proc_side_int
        self.proc_source_int = proc_source_int
        self.proc_guid_int = proc_guid_int
        self.proc_tp_int = proc_tp_int
        self.original_report_txt = original_report_txt
        self.pt_path_id = pt_path_id
        self.histop_core_biopsy_benign_yn = histop_core_biopsy_benign_yn
        self.histop_other_txt = histop_other_txt
        self.histop_benign_bst_parenchyma_yn = histop_benign_bst_parenchyma_yn 
        self.histop_tp_isc_ductal_yn = histop_tp_isc_ductal_yn
        self.histop_tp_isc_other_txt = histop_tp_isc_other_txt
        self.in_situ_nucl_grade_int = in_situ_nucl_grade_int
        self.histop_tp_ic_yn = histop_tp_ic_yn
        self.histop_tp_ic_other_txt = histop_tp_ic_other_txt
        self.histop_other_2_txt = histop_other_2_txt
        
    def __repr__(self):
        return "<gtPathology_record(lesion_id='%s', pt_procedure_id='%s)>" % (self.lesion_id, self.pt_procedure_id)
