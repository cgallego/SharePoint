# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 10:45:23 2017

@author: Cristina Gallego
"""
import sys, os 
import string
import datetime
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# laod Biomatrix engine
from mylocalbase import Base

#  created a patient Biomatrix mapping 
class Pt_record(Base):
    """Base for Pt_record class using Declarative. for table tbl_pt_demographics
    Outputs:
    ========    
    tbl_pt_demographics.pt_id, 
    tbl_pt_demographics.anony_dob_datetime
    
    """
    __tablename__ = 'tbl_pt_demographics'
    __table_args__ = {'autoload':True}
    pt_id = Column(Integer, primary_key=True)
      
    def __repr__(self):
        return "Pt_record: pt_id=%s, mutation_status=%s" % (self.pt_id, self.anony_dob_datetime)


#  created a Cad_record Biomatrix mapping 
class Cad_record(Base):
    """Base for cad_record class using Declarative. for table tbl_pt_mri_cad_record
    Outputs:
    ========
    tbl_pt_mri_cad_record.cad_pt_no_txt, 
    
    tbl_pt_mri_cad_record.latest_mutation_status_int, 
    
    tbl_pt_mri_cad_record.pt_id, 
    """
    __tablename__ = 'tbl_pt_mri_cad_record'
    __table_args__ = {'autoload':True}
    pt_mri_cad_record_id = Column(Integer, primary_key=True)
    pt_id = Column(Integer, ForeignKey('tbl_pt_demographics.pt_id'))
      
    def __repr__(self):
        return "Cad_record: cad_pt_no=%s, mutation_status=%s" % (self.cad_pt_no_txt, self.latest_mutation_status_int)


#  created a Exam_record Biomatrix mapping                              
class Exam_record(Base):
    """Base for Exam_record class using Declarative. for table tbl_pt_exam"""
    __tablename__ = 'tbl_pt_exam'
    __table_args__ = {'autoload':True}
    pt_exam_id = Column(Integer, primary_key=True)
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_id = Column(Integer, ForeignKey('tbl_pt_mri_cad_record.pt_id'))
    cad_record = relationship("Cad_record", backref=backref('tbl_pt_exam', order_by=pt_id))
    
    def __repr__(self):
        return "Exam_record: datetime=%s, a_number_txt=%s, mri_cad_status_txt=%s" % (self.exam_dt_datetime, self.a_number_txt, self.mri_cad_status_txt)


#  created a Exam_Finding Biomatrix mapping                              
class Exam_Finding(Base):
    """Base for Exam_Finding class using Declarative. for table tbl_pt_exam_finding"""
    __tablename__ = 'tbl_pt_exam_finding'
    __table_args__ = {'autoload':True}
    pt_exam_finding_id = Column(Integer, primary_key=True)
    
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_exam_id = Column(Integer, ForeignKey('tbl_pt_exam.pt_id'))
    finding_record = relationship("Exam_record", backref=backref('tbl_pt_exam', order_by=pt_exam_id))
    
    def __repr__(self):
        return "Exam_Finding: mri_mass_yn=%s, mri_nonmass_yn=%s, mri_foci_yn=%s" % (self.mri_mass_yn, self.mri_nonmass_yn, self.mri_foci_yn)
                   
