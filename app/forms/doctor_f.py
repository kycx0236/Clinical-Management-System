from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

class PatientForm(FlaskForm):

    # PATIENT INFORMATION
    firstName = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    midName = StringField('Middle Name', validators=[Length(max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    age = IntegerField('Age', validators=[DataRequired()])
    civilStatus = StringField('Civil Status', validators=[DataRequired(), Length(max=20)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    bloodType = StringField('Blood Type', validators=[Length(max=10)])
    birthPlace = StringField('Birth Place', validators=[Length(max=100)])
    birthDate = DateField('Birth Date (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    p_address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    nationality = StringField('Nationality', validators=[Length(max=20)])
    religion = StringField('Religion', validators=[DataRequired(), Length(max=50)])
    eContactName = StringField('Emergency Contact One', validators=[Length(max=20)])
    relationship = StringField('Relationship One', validators=[Length(max=20)])
    eContactNum = StringField('Contact Number One', validators=[Length(max=20)])
    occupation = StringField('Occupation', validators=[Length(max=50)])
    p_email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    p_contactNum = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])

    # MEDICAL HISTORY
    bcgCheckbox = BooleanField('BCG Checkbox', default=False)
    dtpCheckbox = BooleanField('DTP Checkbox', default=False)
    pcvCheckbox = BooleanField('PCV Checkbox', default=False)
    influenzaCheckbox = BooleanField('Influenza Checkbox', default=False)
    hepaCheckbox = BooleanField('Hepa Checkbox', default=False)
    ipvCheckbox = BooleanField('IPV Checkbox', default=False)
    mmrCheckbox = BooleanField('MMR Checkbox', default=False)
    hpvCheckbox = BooleanField('HPV Checkbox', default=False)
    asthmaCheckbox = BooleanField('Asthma Checkbox', default=False)
    diabetesCheckbox = BooleanField('Diabetes Checkbox', default=False)
    heartCheckbox = BooleanField('Heart Checkbox', default=False)
    birthCheckbox = BooleanField('Birth Checkbox', default=False)
    boneCheckbox = BooleanField('Bone Checkbox', default=False)
    alzheimerCheckbox = BooleanField('Alzheimer Checkbox', default=False)
    cancerCheckbox = BooleanField('Cancer Checkbox', default=False)
    thyroidCheckbox = BooleanField('Thyroid Checkbox', default=False)
    tuberculosisCheckbox = BooleanField('Tuberculosis Checkbox', default=False)
    eyeCheckbox = BooleanField('Eye Checkbox', default=False)
    clotsCheckbox = BooleanField('Clots Checkbox', default=False)
    mentalCheckbox = BooleanField('Mental Checkbox', default=False)
    kidneyCheckbox = BooleanField('Kidney Checkbox', default=False)
    anemiaCheckbox = BooleanField('Anemia Checkbox', default=False)
    muscleCheckbox = BooleanField('Muscle Checkbox', default=False)
    highbloodCheckbox = BooleanField('Highblood Checkbox', default=False)
    epilepsyCheckbox = BooleanField('Epilepsy Checkbox', default=False)
    skinCheckbox = BooleanField('Skin Checkbox', default=False)
    hivCheckbox = BooleanField('HIV Checkbox', default=False)
    pulmonaryCheckbox = BooleanField('Pulmonary Checkbox', default=False)

    specifications = TextAreaField('Specifications')
    others = TextAreaField('Others')

    past_c1 = StringField('Past Condition 1', validators=[Length(max=255)])
    medication1 = StringField('Medication 1', validators=[Length(max=255)])
    dosage1 = StringField('Dosage 1', validators=[Length(max=255)])
    h_date1 = DateField('Date 1', format='%Y-%m-%d')
    
    past_c2 = StringField('Past Condition 2', validators=[Length(max=255)])
    medication2 = StringField('Medication 2', validators=[Length(max=255)])
    dosage2 = StringField('Dosage 2', validators=[Length(max=255)])
    h_date2 = DateField('Date 2', format='%Y-%m-%d')
    
    past_c3 = StringField('Past Condition 3', validators=[Length(max=255)])
    medication3 = StringField('Medication 3', validators=[Length(max=255)])
    dosage3 = StringField('Dosage 3', validators=[Length(max=255)])
    h_date3 = DateField('Date 3', format='%Y-%m-%d')

    habitually = StringField('Habitually', validators=[Length(max=10)])
    yearsDrunk = IntegerField('Years Drunk')
    frequencyDrink = StringField('Frequency Drink', validators=[Length(max=255)])
    quitDrinking = IntegerField('Quit Drinking')

    frequently = StringField('Frequently', validators=[Length(max=10)])
    yearsSmoked = IntegerField('Years Smoked')
    frequencySmoke = StringField('Frequency Smoke', validators=[Length(max=255)])
    quitSmoking = IntegerField('Quit Smoking')

    often = StringField('Often', validators=[Length(max=10)])
    exerciseType = StringField('Exercise Type', validators=[Length(max=255)])
    frequencyExercise = StringField('Frequency Exercise', validators=[Length(max=255)])
    durationActivity = StringField('Duration Activity', validators=[Length(max=255)])

    sexActive = StringField('Sex Active', validators=[Length(max=10)])
    sexPartner = StringField('Sex Partner', validators=[Length(max=10)])
    numSexPartner = IntegerField('Number of Sex Partner')
    contraception = StringField('Contraception', validators=[Length(max=255)])

    useDrugs = StringField('Use Drugs', validators=[Length(max=10)])
    specifyDrugs = StringField('Specify Drugs', validators=[Length(max=255)])
    frequencyDrugs = StringField('Frequency Drugs', validators=[Length(max=255)])

    surgeryDate1 = DateField('Surgery Date 1', format='%Y-%m-%d')
    surgeryProcedure1 = StringField('Surgery Procedure 1', validators=[Length(max=255)])
    hospital1 = TextAreaField('Hospital 1')
    
    surgeryDate2 = DateField('Surgery Date 2', format='%Y-%m-%d')
    surgeryProcedure2 = StringField('Surgery Procedure 2', validators=[Length(max=255)])
    hospital2 = TextAreaField('Hospital 2')
    
    surgeryDate3 = DateField('Surgery Date 3', format='%Y-%m-%d')
    surgeryProcedure3 = StringField('Surgery Procedure 3', validators=[Length(max=255)])
    hospital3 = TextAreaField('Hospital 3')
    
    medications = TextAreaField('Medications')
    allergies = TextAreaField('Allergies')

    # MEDICAL ASSESSMENT
    subject = StringField('Subject', validators=[DataRequired(), Length(max=255)])
    complaints = TextAreaField('Complaints')
    illnessHistory = StringField('Illness History', validators=[Length(max=255)])
    bloodPressure = StringField('Blood Pressure', validators=[Length(max=100)])
    pulseRate = StringField('Pulse Rate', validators=[Length(max=100)])
    temperature = StringField('Temperature', validators=[Length(max=100)])
    respRate = StringField('Respiratory Rate', validators=[Length(max=100)])
    height = StringField('Height', validators=[Length(max=50)])
    weight = StringField('Weight', validators=[Length(max=50)])
    bmi = StringField('BMI', validators=[Length(max=50)])
    normal_head = StringField('Normal Head', validators=[Length(max=50)])
    abnormalities_head = StringField('Abnormalities Head', validators=[Length(max=255)])
    normal_ears = StringField('Normal Ears', validators=[Length(max=50)])
    abnormalities_ears = StringField('Abnormalities Ears', validators=[Length(max=255)])
    normal_eyes = StringField('Normal Eyes', validators=[Length(max=50)])
    abnormalities_eyes = StringField('Abnormalities Eyes', validators=[Length(max=255)])
    normal_nose = StringField('Normal Nose', validators=[Length(max=50)])
    abnormalities_nose = StringField('Abnormalities Nose', validators=[Length(max=255)])
    normal_skin = StringField('Normal Skin', validators=[Length(max=50)])
    abnormalities_skin = StringField('Abnormalities Skin', validators=[Length(max=255)])
    normal_back = StringField('Normal Back', validators=[Length(max=50)])
    abnormalities_back = StringField('Abnormalities Back', validators=[Length(max=255)])
    normal_neck = StringField('Normal Neck', validators=[Length(max=50)])
    abnormalities_neck = StringField('Abnormalities Neck', validators=[Length(max=255)])
    normal_throat = StringField('Normal Throat', validators=[Length(max=50)])
    abnormalities_throat = StringField('Abnormalities Throat', validators=[Length(max=255)])
    normal_chest = StringField('Normal Chest', validators=[Length(max=50)])
    abnormalities_chest = StringField('Abnormalities Chest', validators=[Length(max=255)])
    normal_abdomen = StringField('Normal Abdomen', validators=[Length(max=50)])
    abnormalities_abdomen = StringField('Abnormalities Abdomen', validators=[Length(max=255)])
    normal_upper = StringField('Normal Upper Body', validators=[Length(max=50)])
    abnormalities_upper = StringField('Abnormalities Upper Body', validators=[Length(max=255)])
    normal_lower = StringField('Normal Lower Body', validators=[Length(max=50)])
    abnormalities_lower = StringField('Abnormalities Lower Body', validators=[Length(max=255)])
    normal_tract = StringField('Normal Tract', validators=[Length(max=50)])
    abnormalities_tract = StringField('Abnormalities Tract', validators=[Length(max=255)])
    comments = TextAreaField('Comments')
    diagnosis = TextAreaField('Diagnosis')
    consultationDate = DateTimeField('Consultation Date', format='%Y-%m-%dT%H:%M:%S')

    # PRESCRIPTION DETAILS
    medication_name = StringField('Medication Name', validators=[Length(max=255)])
    dosage = StringField('Dosage', validators=[Length(max=255)])
    p_quantity = StringField('Prescribed Quantity', validators=[Length(max=255)])
    duration = StringField('Duration', validators=[Length(max=255)])
    instructions = StringField('Instructions', validators=[Length(max=255)])

    # LABORATORY JOB ORDER
    patientName = StringField('Patient Name', validators=[DataRequired(), Length(max=255)])
    labSubject = StringField('Lab Subject', validators=[DataRequired(), Length(max=255)])
    gender = StringField('Gender', validators=[DataRequired(), Length(max=10)])
    age = StringField('Age', validators=[DataRequired(), Length(max=10)])
    physician = StringField('Physician', validators=[DataRequired(), Length(max=255)])
    orderDate = StringField('Order Date', validators=[DataRequired(), Length(max=20)])
    otherTest = StringField('Other Test', validators=[Length(max=255)])

    # HEMATOLOGY
    cbcplateCheckbox = BooleanField('CBC Plate Checkbox', default=False)
    hgbhctCheckbox = BooleanField('HGB/HCT Checkbox', default=False)
    protimeCheckbox = BooleanField('Protime Checkbox', default=False)
    APTTCheckbox = BooleanField('APTT Checkbox', default=False)
    bloodtypingCheckbox = BooleanField('Blood Typing Checkbox', default=False)
    ESRCheckbox = BooleanField('ESR Checkbox', default=False)
    plateCheckbox = BooleanField('Plate Checkbox', default=False)
    hgbCheckbox = BooleanField('HGB Checkbox', default=False)
    hctCheckbox = BooleanField('HCT Checkbox', default=False)
    cbcCheckbox = BooleanField('CBC Checkbox', default=False)
    reticsCheckbox = BooleanField('Retics Checkbox', default=False)
    CTBTCheckbox = BooleanField('CTBT Checkbox', default=False)

    # BACTERIOLOGY
    culsenCheckbox = BooleanField('Culsen Checkbox', default=False)
    cultureCheckbox = BooleanField('Culture Checkbox', default=False)
    gramCheckbox = BooleanField('Gram Checkbox', default=False)
    KOHCheckbox = BooleanField('KOH Checkbox', default=False)

    # HISTOPATHOLOGY
    biopsyCheckbox = BooleanField('Biopsy Checkbox', default=False)
    papsCheckbox = BooleanField('Paps Checkbox', default=False)
    FNABCheckbox = BooleanField('FNAB Checkbox', default=False)
    cellCheckbox = BooleanField('Cell Checkbox', default=False)
    cytolCheckbox = BooleanField('Cytol Checkbox', default=False)

    # CLINICAL MIRCROSCOPY & PARASITOLOGY
    urinCheckbox = BooleanField('Urin Checkbox', default=False)
    stoolCheckbox = BooleanField('Stool Checkbox', default=False)
    occultCheckbox = BooleanField('Occult Checkbox', default=False)
    semenCheckbox = BooleanField('Semen Checkbox', default=False)
    ELISACheckbox = BooleanField('ELISA Checkbox', default=False)

    # SEROLOGY
    ASOCheckbox = BooleanField('ASO', default=False)
    AntiHBSCheckbox = BooleanField('Anti-HBS', default=False)
    HCVCheckbox = BooleanField('HCV', default=False)
    C3Checkbox = BooleanField('C3', default=False)
    HIVICheckbox = BooleanField('HIV I', default=False)
    HIVIICheckbox = BooleanField('HIV II', default=False)
    NS1Checkbox = BooleanField('NS1', default=False)
    VDRLCheckbox = BooleanField('VDRL', default=False)
    PregCheckbox = BooleanField('Pregnancy Test', default=False)
    RFCheckbox = BooleanField('RF', default=False)
    QuantiCheckbox = BooleanField('Quanti', default=False)
    QualiCheckbox = BooleanField('Quali', default=False)
    TyphidotCheckbox = BooleanField('Typhidot', default=False)
    TubexCheckbox = BooleanField('Tubex', default=False)
    HAVIgMCheckbox = BooleanField('HAV IgM', default=False)
    DengueCheckbox = BooleanField('Dengue', default=False)

    # IMMUNOCHEMISTRY
    AFPCheckbox = BooleanField('AFP', default=False)
    ferritinCheckbox = BooleanField('Ferritin', default=False)
    HBcIgMCheckbox = BooleanField('HBc IgM', default=False)
    AntiHBECheckbox = BooleanField('Anti-HBE', default=False)
    CA125Checkbox = BooleanField('CA-125', default=False)
    PROBNPCheckbox = BooleanField('PRO BNP', default=False)
    CA153Checkbox = BooleanField('CA-153', default=False)
    CA199Checkbox = BooleanField('CA-199', default=False)
    PSACheckbox = BooleanField('PSA', default=False)
    CEACheckbox = BooleanField('CEA', default=False)
    FreeT3Checkbox = BooleanField('Free T3', default=False)
    ANA2Checkbox = BooleanField('ANA 2', default=False)
    FreeT4Checkbox = BooleanField('Free T4', default=False)
    HBsAGCheckbox = BooleanField('HBsAG', default=False)
    TroponiniCheckbox = BooleanField('Troponin I', default=False)
    HbACheckbox = BooleanField('HbA', default=False)
    HBAeAgCheckbox = BooleanField('HBAeAg', default=False)
    BetaCheckbox = BooleanField('Beta', default=False)
    T3Checkbox = BooleanField('T3', default=False)
    T4Checkbox = BooleanField('T4', default=False)
    TSHCheckbox = BooleanField('TSH', default=False)

    # CLINICAL CHEMISTRY
    ALPCheckbox = BooleanField('ALP', default=False)
    AmylaseCheckbox = BooleanField('Amylase', default=False)
    BUACheckbox = BooleanField('BUA', default=False)
    BUNCheckbox = BooleanField('BUN', default=False)
    CreatinineCheckbox = BooleanField('Creatinine', default=False)
    SGPTCheckbox = BooleanField('SGPT', default=False)
    SGOTCheckbox = BooleanField('SGOT', default=False)
    FBSCheckbox = BooleanField('FBS', default=False)
    RBSCheckbox = BooleanField('RBS', default=False)
    HPPCheckbox = BooleanField('HPP', default=False)
    OGCTCheckbox = BooleanField('OGCT', default=False)
    HGTCheckbox = BooleanField('HGT', default=False)
    OGTTCheckbox = BooleanField('OGTT', default=False)
    NaCheckbox = BooleanField('Na', default=False)
    MgCheckbox = BooleanField('Mg', default=False)
    LipidCheckbox = BooleanField('Lipid', default=False)
    TriglyCheckbox = BooleanField('Triglycerides', default=False)
    CholCheckbox = BooleanField('Cholesterol', default=False)
    ClCheckbox = BooleanField('Cl', default=False)
    TPAGCheckbox = BooleanField('TPAG', default=False)
    TotalCheckbox = BooleanField('Total Protein', default=False)
    GlobCheckbox = BooleanField('Globulin', default=False)
    AlbCheckbox = BooleanField('Albumin', default=False)
    CKMBCheckbox = BooleanField('CK-MB', default=False)
    CKTotalCheckbox = BooleanField('CK Total', default=False)
    LDHCheckbox = BooleanField('LDH', default=False)
    KCheckbox = BooleanField('K', default=False)
    CaCheckbox = BooleanField('Ca', default=False)
    IonizedCheckbox = BooleanField('Ionized', default=False)
    PhosCheckbox = BooleanField('Phosphorus', default=False)

    submit = SubmitField('Submit')