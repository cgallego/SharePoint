# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 09:23:24 2017

----------------------------------------------------------------------
@ Copyright (C) Cristina Gallego, University of Toronto, 2017
----------------------------------------------------------------------
"""
            
if __name__ == '__main__':
    ############################
    from query_biomatrix_database import *
    from add_newrecords import *
    
    ## initialize query
    print "\n Querying a case in Biomatrix..."
    query = Query_biomatrix()
    # define query patient parameters
    StudyID = '25'.zfill(4)
    AccessionN = '7002835'
    # Now query for tabulated exam findings (accession required)
    # this returns query.findreport with lesion info
    findreport, radioinfo, massreport, nonmassreport, focireport = query.queryExamFindings(StudyID, AccessionN)
    print(findreport['exam.original_report'][0])
    print(radioinfo)

    # query exam finding if procedure 
    # this return query.gtpathology
    gtpathology = query.queryifProcedure(StudyID, AccessionN)
    
    #############################
    # Send record to local db
    print "\n Adding record case to local DB..."
    newrecords = AddNewRecords()      
    # submit thiese case with lesion_id =1
    lesion_id = 1 # you will need to autoincrement with more findings
    newrecords.lesion_2DB( findreport.iloc[0] )

    newrecords.radiology_2DB(lesion_id, radioinfo.iloc[0])
    newrecords.gtpathology_2DB(lesion_id, gtpathology.iloc[0]  )
