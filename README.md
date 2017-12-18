
# Contents
## Code examples inside databases folder

This documentation serves as a walk-through the code/utilities/workflow and in general tips included in each directory

### 1) To query Biomatrix Database
* First, start by setting up a simple easy-to-use graphical query tool.
* You will need to install [pgAdmin](https://www.pgadmin.org/download/) - 
* Then set up the biomatrix server configuration (not shared publicly - ask me for user info)
* Once connected to the server, use que SQL graphical query tool to map tables and create queries. Here is an SQL query example to retrieve all non-mass findings in breast MRI since 2011 that have an associated hispopathology procedure :

```
SELECT 
  tbl_pt_exam.pt_id, 
  tbl_pt_mri_cad_record.pt_mri_cad_record_id, 
  tbl_pt_mri_cad_record.cad_pt_no_txt, 
  tbl_pt_exam.exam_dt_datetime, 
  tbl_pt_exam.a_number_txt, 
  tbl_pt_exam.mri_cad_status_txt, 
  tbl_pt_exam.original_report_txt, 
  tbl_pt_exam_finding.mri_nonmass_yn, 
  tbl_pt_exam_finding.mri_nonmass_dist_int, 
  tbl_pt_exam_finding.mri_nonmass_int_enh_int, 
  tbl_pt_exam_finding.mri_o_find_cysts_yn, 
  tbl_pt_procedure.proc_dt_datetime, 
  tbl_pt_pathology.histop_core_biopsy_benign_yn, 
  tbl_pt_pathology.tumr_site_int, 
  tbl_pt_pathology.histop_tp_ic_yn, 
  tbl_pt_pathology.histop_tp_isc_ductal_yn, 
  tbl_pt_pathology.in_situ_nucl_grade_int
FROM 
  public.tbl_pt_exam, 
  public.tbl_pt_mri_cad_record, 
  public.tbl_pt_exam_finding, 
  public.tbl_pt_procedure, 
  public.tbl_pt_pathology, 
  public.tbl_pt_path_exam_find_link
WHERE 
  tbl_pt_exam.pt_exam_id = tbl_pt_exam_finding.pt_exam_id AND
  tbl_pt_mri_cad_record.pt_id = tbl_pt_exam.pt_id AND
  tbl_pt_mri_cad_record.pt_id = tbl_pt_procedure.pt_id AND
  tbl_pt_pathology.pt_procedure_id = tbl_pt_procedure.pt_procedure_id AND
  tbl_pt_path_exam_find_link.pt_path_id = tbl_pt_pathology.pt_path_id AND
  tbl_pt_path_exam_find_link.pt_exam_finding_id = tbl_pt_exam_finding.pt_exam_finding_id AND
  tbl_pt_exam.exam_dt_datetime > '2011-01-01' AND 
  tbl_pt_exam_finding.mri_nonmass_yn = TRUE
ORDER BY
  tbl_pt_mri_cad_record.cad_pt_no_txt ASC;

```

### 2) To query biomatrix through back end access (using python/sqlalchemy)
* Clone code in /databases folder
* In your Python distribution, install [SQLalchemy]( http://docs.sqlalchemy.org/en/latest/intro.html) package:
```
pip install sqlalchemy 
pip install psycopg2
```
* See an example on how to query biomatrix through the back-end in python file query_biomatrix_database.py. Examples show how to:
* Query to retrieve radiology reports
* Query to retrieve pathology/procedure reports (if they exist)
* Notice you can wrap SQL queries directly into a pandas Dataframe (recommended but tkes usually longer. Can also select specific columns, more efficient):
```
e.g: pd.read_sql_query('SELECT * FROM data', engine)
```
* code examples show how to wrap the sql schema into a python object then 
retrieves selected table data

### 3) To create a local database with partial biomatrix records and your own (e.g feature sets per lesion)
* Run a script that creates your schema (see createDatabase.py)
* Then, you're ready to query biomatrix and select which records to save locally for easy access or to  combined them with bank of features (run query_and_savelocaldb.py)
* code provided shows examples of how to send records to the local database you just created
* Use [sqlitestudio - version tested 2.1.5](http://sqlitestudio.one.pl/index.rvt?act=download)  graphical tool to see your local database and manipulate/export/create views etc...



