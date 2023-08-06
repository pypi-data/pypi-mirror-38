from ambition_form_validators import HEADACHE, VISUAL_LOSS
from edc_constants.constants import OTHER, NORMAL, NONE
from edc_list_data import PreloadData

list_data = {
    'ambition_lists.antibiotic': [
        ('flucloxacillin', 'Flucloxacillin'),
        ('gentamicin', 'Gentamicin'),
        ('ceftriaxone', 'Ceftriaxone'),
        ('amoxicillin_ampicillin', 'Amoxicillin/Ampicillin'),
        ('doxycycline', 'Doxycycline'),
        ('erythromycin', 'Erythromycin'),
        ('ciprofloxacin', 'Ciprofloxacin'),
        (OTHER, 'Other, specify')
    ],
    'ambition_lists.neurological': [
        ('meningism', 'Meningism'),
        ('papilloedema', ' Papilloedema'),
        ('focal_neurologic_deficit', 'Focal neurologic deficit'),
        ('CN_VI_palsy', 'Cranial Nerve VI palsy'),
        ('CN_III_palsy', 'Cranial Nerve III palsy'),
        ('CN_IV_palsy', 'Cranial Nerve IV palsy'),
        ('CN_VII_palsy', 'Cranial Nerve VII palsy'),
        ('CN_VIII_palsy', 'Cranial Nerve VIII palsy'),
        (OTHER, 'Other CN palsy'),
    ],
    'ambition_lists.day14medication': [
        ('fluconazole', 'Fluconazole'),
        ('rifampicin', ' Rifampicin'),
        ('co_trimoxazole', 'Co-trimoxazole'),
        (OTHER, 'Other')
    ],
    'ambition_lists.medication': [
        ('TMP-SMX', 'TMP-SMX'),
        (OTHER, 'Other, specify;')
    ],
    'ambition_lists.otherdrug': [
        ('potassium', ' Potassium'),
        ('magnesium', 'Magnesium'),
        ('vitamins', ' Vitamins'),
        ('tmp_smx_Cotrimoxazole', ' TMP-SMX/Cotrimoxazole'),
        ('anti_convulsants', 'Anticonvulsants'),
        ('antibiotics', 'Antibiotics'),
        (NONE, 'None, no other drugs/interventions given'),
        (OTHER, 'Other, specify')
    ],
    'ambition_lists.significantnewdiagnosis': [
        ('tb_pulmonary', 'TB pulmonary'),
        ('kaposi_sarcoma', 'Kaposi’s sarcoma'),
        ('bacteraemia', 'Bacteraemia'),
        ('diarrhoeal_wasting', 'Diarrhoeal wasting'),
        ('tb_extra_pulmonary', 'TB extra-pulmonary'),
        ('malaria', 'Malaria'),
        ('bacterial_pneumonia', 'Bacterial pneumonia'),
        (OTHER, 'Other, please specify:'),
    ],
    'ambition_lists.symptom': [
        ('cough', 'Cough'),
        (HEADACHE, 'Headache'),
        ('double_vision', 'Double vision'),
        (VISUAL_LOSS, 'Visual loss'),
        ('fever', 'Fever'),
        ('hearing_loss', 'Hearing loss'),
        ('confusion', 'Confusion'),
        ('drowsiness', 'Drowsiness'),
        ('behaviour_change', 'Behaviour change'),
        ('focal_weakness', 'Focal weakness'),
        ('seizures_lt_72 hrs', 'Seizures (<72 hrs)'),
        ('seizures_gt_72', 'Seizures (72 hrs - 1 mo)'),
        ('nausea', 'Nausea'),
        ('vomiting', 'Vomiting'),
        ('weight_loss', 'Weight loss'),
        ('skin_lesions', 'Skin lesions'),
        ('shortness_of_breath', 'Shortness of breath'),
    ],
    'ambition_lists.abnormalresultsreason': [
        ('cerebral_oedema', 'Cerebral oedema'),
        ('hydrocephalus', 'Hydrocephalus'),
        ('cryptococcomas', 'Cryptococcomas'),
        ('dilated_virchow_robin_spaces', 'Dilated Virchow-Robin spaces'),
        ('enhancing_mass_lesions',
         'Enhancing mass lesions DD toxoplasmosis, TB, lymphoma'),
        ('infarcts', 'Infarcts'),
        (OTHER, 'Other'),
    ],
    'ambition_lists.cxrtype': [
        (NORMAL, 'Normal'),
        ('hilar_adenopathy', 'Hilar adenopathy'),
        ('miliary_appearance', 'Miliary appearance'),
        ('pleural_effusion', 'Pleural effusion'),
        ('infiltrates', 'Infiltrates'),
    ],
    'ambition_lists.infiltratelocation': [
        ('lul', 'LUL'),
        ('lll', 'LLL'),
        ('rul', 'RUL'),
        ('rll', 'RLL'),
        ('rml', 'RML'),
        ('diffuse', 'Diffuse'),
    ],
    'ambition_lists.misseddoses': [
        ('dose_1', 'Dose 1'),
        ('dose_2', 'Dose 2'),
        ('dose_3', 'Dose 3'),
        ('dose_4', 'Dose 4')
    ],
}


preload_data = PreloadData(list_data=list_data)
