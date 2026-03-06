"""
═══════════════════════════════════════════════════════════════════════════════
TKM Patient Generator - PDF Export Utility
한의 임상 가상환자 시나리오 PDF 내보내기
═══════════════════════════════════════════════════════════════════════════════
"""

import io
from datetime import datetime
from fpdf import FPDF


class KoreanPDF(FPDF):
    """PDF class with Korean font support."""
    
    def __init__(self):
        super().__init__()
        # Use built-in font that supports more characters
        # For full Korean support, we'll use unicode mode
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
    
    def header(self):
        """Add header to each page."""
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'TKM Patient Generator', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(5)
    
    def footer(self):
        """Add footer with page number."""
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_patient_pdf(summary: str, scenario: str, patient_info: dict = None) -> bytes:
    """
    Generate a PDF document for the patient scenario.
    
    Args:
        summary: Patient summary text
        scenario: Full patient scenario text
        patient_info: Optional dictionary with patient metadata
    
    Returns:
        PDF file as bytes
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, 'Virtual Patient Case Report', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 10, '(Han-ui Clinical Scenario Generator)', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    
    # Generation timestamp
    pdf.set_font('Helvetica', 'I', 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f'Generated: {timestamp}', align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    
    # Divider line
    pdf.set_draw_color(100, 100, 100)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Patient info section (if provided)
    if patient_info:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, 'Patient Information', new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 10)
        
        # Use _make_safe_text for Korean values
        disease = _make_safe_text(str(patient_info.get('disease', 'N/A')))
        pattern = _make_safe_text(str(patient_info.get('pattern', 'N/A')))
        sex = _make_safe_text(str(patient_info.get('sex', 'N/A')))
        
        info_items = [
            ('Disease', disease),
            ('Pattern', pattern),
            ('Age/Sex', f"{patient_info.get('age', 'N/A')} / {sex}"),
            ('Height/Weight', f"{patient_info.get('height', 'N/A')}cm / {patient_info.get('weight', 'N/A')}kg"),
            ('Vitals', f"BP {patient_info.get('sbp', 'N/A')}/{patient_info.get('dbp', 'N/A')} mmHg, "
                      f"HR {patient_info.get('pulse_rate', 'N/A')}/min, "
                      f"Temp {patient_info.get('temp', 'N/A')}C"),
        ]
        
        for label, value in info_items:
            pdf.cell(40, 6, f'{label}:', new_x='RIGHT')
            safe_value = _make_safe_text(str(value)) if not isinstance(value, (int, float)) else str(value)
            pdf.cell(0, 6, safe_value, new_x='LMARGIN', new_y='NEXT')
        
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
    
    # Summary section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Summary', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    
    # Handle Korean text by encoding/replacing unsupported characters
    safe_summary = _make_safe_text(summary)
    pdf.multi_cell(0, 6, safe_summary)
    pdf.ln(5)
    
    # Scenario section
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Patient Scenario', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 10)
    
    # Process scenario text - handle Korean characters
    safe_scenario = _make_safe_text(scenario)
    
    # Split into paragraphs and add each
    paragraphs = safe_scenario.split('\n')
    for para in paragraphs:
        para = para.strip()
        if para:
            # Check if this is a section header (starts with special chars)
            if para.startswith('[') or para.startswith('【') or para.startswith('-'):
                pdf.set_font('Helvetica', 'B', 10)
                pdf.multi_cell(0, 6, para)
                pdf.set_font('Helvetica', '', 10)
            else:
                pdf.multi_cell(0, 6, para)
            pdf.ln(2)
    
    # Output as bytes (convert bytearray to bytes for Streamlit)
    output = pdf.output()
    if isinstance(output, bytearray):
        return bytes(output)
    elif isinstance(output, bytes):
        return output
    else:
        return output.encode('latin-1') if isinstance(output, str) else bytes(output)


def _make_safe_text(text: str) -> str:
    """
    Convert Korean text to a safe format for PDF.
    Since basic FPDF doesn't support Korean well, we'll create a 
    transliteration/replacement approach for common patterns.
    
    For full Korean support, consider using fonts like NanumGothic.
    """
    if not text:
        return ""
    
    # Common Korean medical terms mapping to romanization/English
    replacements = {
        # Section markers
        '【': '[',
        '】': ']',
        '→': '->',
        '°': ' deg ',
        
        # Disease names (질환명)
        '감기': 'Common Cold',
        '알레르기비염': 'Allergic Rhinitis',
        '기능성소화불량': 'Functional Dyspepsia',
        '기능성 소화불량': 'Functional Dyspepsia',
        '요통': 'Low Back Pain',
        
        # Common medical terms (한의학)
        '환자정보': '[Patient Info]',
        '주소증': '[Chief Complaint]',
        '현병력': '[Present Illness]',
        '과거력': '[Past History]',
        '가족력': '[Family History]',
        '사회력': '[Social History]',
        '계통적 문진': '[Review of Systems]',
        '신체검진 소견': '[Physical Exam]',
        '설진 소견': '[Tongue Exam]',
        '맥진 소견': '[Pulse Exam]',
        '활력징후': 'Vital Signs',
        
        # Common symptoms
        '발열': 'Fever',
        '오한': 'Chills',
        '두통': 'Headache',
        '기침': 'Cough',
        '콧물': 'Runny nose',
        '인후통': 'Sore throat',
        '몸살': 'Body ache',
        '요통': 'Low back pain',
        '소화불량': 'Dyspepsia',
        '복통': 'Abdominal pain',
        '오심': 'Nausea',
        '구토': 'Vomiting',
        '설사': 'Diarrhea',
        '변비': 'Constipation',
        
        # Demographics
        '남': 'M',
        '여': 'F',
        '세': 'y/o',
        
        # Common descriptors
        '없음': 'None',
        '있음': 'Present',
        '경미': 'Mild',
        '중등도': 'Moderate', 
        '심함': 'Severe',
        '정상': 'Normal',
        '보통': 'Normal',
        
        # Vitals
        '수축기혈압': 'SBP',
        '이완기혈압': 'DBP',
        '맥박': 'HR',
        '체온': 'Temp',
        '호흡': 'RR',
        
        # Time
        '일 전': ' days ago',
        '주 전': ' weeks ago',
        '개월 전': ' months ago',
        '시간': 'hours',
        '분': 'min',
        '회': 'times',
        
        # Pattern names
        '풍한형': 'Wind-Cold',
        '풍열형': 'Wind-Heat',
        '풍조형': 'Wind-Dryness',
        '한증형': 'Cold Pattern',
        '열증형': 'Heat Pattern',
        '기허형': 'Qi Deficiency',
        '양허형': 'Yang Deficiency',
        '음허형': 'Yin Deficiency',
        '담음형': 'Phlegm-Fluid',
        '식적형': 'Food Stagnation',
        '어혈형': 'Blood Stasis',
        '기체형': 'Qi Stagnation',
        
        # 요통 patterns
        '신허형': 'Kidney Deficiency',
        '풍한습비형': 'Wind-Cold-Damp',
        '어혈형': 'Blood Stasis',
        '습열형': 'Damp-Heat',
        
        # 소화불량 patterns  
        '간위불화형': 'Liver-Stomach Disharmony',
        '비위허약형': 'Spleen-Stomach Deficiency',
        '음식정체형': 'Food Stagnation',
        '위음부족형': 'Stomach Yin Deficiency',
        
        # Pattern with prescription (처방)
        '오적산': 'Ojeoksan',
        '갈근탕': 'Galgeuntang',
        '삼소음': 'Samsoeum',
        '소청룡탕': 'Socheongnyongtang',
        '형개연교탕': 'Hyeonggaeyeongyotang',
        '보중익기탕': 'Bojungikgitang',
        '평위산': 'Pyeongwisan',
        '소요산': 'Soyosan',
        '육군자탕': 'Yukgunja-tang',
        '독활기생탕': 'Dokhwalgisaengtang',
        '신기환': 'Singihwan',
        
        # Tongue/Pulse
        '설질': 'Tongue body',
        '설태': 'Tongue coating',
        '부맥': 'Floating pulse',
        '침맥': 'Sinking pulse',
        '중맥': 'Middle pulse',
        '세맥': 'Thin pulse',
        '대맥': 'Large pulse',
        '홍맥': 'Flooding pulse',
        '유력': 'Strong',
        '무력': 'Weak',
        '강력': 'Very Strong',
        '활맥': 'Slippery pulse',
        '완맥': 'Moderate pulse',
        '삽맥': 'Rough pulse',
        '유맥': 'Soft pulse',
        '긴맥': 'Tense pulse',
        '담백': 'Pale',
        '담홍': 'Pale red',
        '홍설': 'Red',
        '강홍': 'Dark red',
        '자설': 'Purple',
        '백태': 'White coating',
        '황태': 'Yellow coating',
        '회태': 'Grey coating',
        '박태': 'Thin coating',
        '후태': 'Thick coating',
        '니태': 'Greasy coating',
        '조태': 'Dry coating',
        '윤태': 'Moist coating',
        '활태': 'Wet coating',
        '소': 'Small',
        '정상': 'Normal',
        '대/태': 'Enlarged',
    }
    
    result = text
    for korean, english in replacements.items():
        result = result.replace(korean, english)
    
    # Remove any remaining non-ASCII characters that FPDF can't handle
    # This is a fallback - ideally we'd use a Korean-supporting font
    try:
        result = result.encode('ascii', 'replace').decode('ascii')
    except:
        result = ''.join(c if ord(c) < 128 else '?' for c in result)
    
    return result


def _make_safe_value(value) -> str:
    """Convert any value to ASCII-safe string for PDF."""
    if value is None:
        return "N/A"
    text = str(value)
    return _make_safe_text(text)


def generate_patient_pdf_korean(summary: str, scenario: str, patient_info: dict = None) -> bytes:
    """
    Generate a PDF document with Korean support using bundled NanumGothic font.
    
    Args:
        summary: Patient summary text  
        scenario: Full patient scenario text
        patient_info: Optional dictionary with patient metadata
    
    Returns:
        PDF file as bytes
    """
    import pathlib
    import tempfile
    
    # Try to create PDF with Unicode support
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Temp directory for font (writable on all platforms)
    temp_dir = pathlib.Path(tempfile.gettempdir())
    temp_font_path = temp_dir / "NanumGothic.ttf"
    
    # Get the directory where this script is located
    script_dir = pathlib.Path(__file__).parent.resolve()
    
    # Korean font source paths to check (in priority order)
    font_sources = [
        # System-installed fonts (via packages.txt on Streamlit Cloud)
        pathlib.Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        pathlib.Path("/usr/share/fonts/opentype/nanum/NanumGothic.ttf"),
        # Bundled font (local development)
        script_dir / "fonts" / "NanumGothic.ttf",
        pathlib.Path.cwd() / "fonts" / "NanumGothic.ttf",
        # Windows system fonts
        pathlib.Path("C:/Windows/Fonts/malgun.ttf"),
        pathlib.Path("C:/Windows/Fonts/NanumGothic.ttf"),
    ]
    
    font_added = False
    
    # First check if font already in temp (from previous run)
    if temp_font_path.exists():
        try:
            pdf.add_font("Korean", "", str(temp_font_path), uni=True)
            pdf.set_font("Korean", "", 12)
            font_added = True
        except Exception:
            temp_font_path.unlink(missing_ok=True)
    
    # If not in temp, try each source
    if not font_added:
        for font_path in font_sources:
            if font_path.exists():
                try:
                    # Try using font directly first (works for system fonts)
                    pdf.add_font("Korean", "", str(font_path), uni=True)
                    pdf.set_font("Korean", "", 12)
                    font_added = True
                    break
                except PermissionError:
                    # If permission denied, try copying to temp
                    try:
                        with open(font_path, 'rb') as src:
                            font_data = src.read()
                        with open(temp_font_path, 'wb') as dst:
                            dst.write(font_data)
                        pdf.add_font("Korean", "", str(temp_font_path), uni=True)
                        pdf.set_font("Korean", "", 12)
                        font_added = True
                        break
                    except Exception:
                        continue
                except Exception:
                    continue
    
    if not font_added:
        # Fallback to ASCII version if no Korean font found
        return generate_patient_pdf(summary, scenario, patient_info)
    
    # Title
    pdf.set_font('Korean', '', 16)
    pdf.cell(0, 10, '한의 임상 가상환자 시나리오', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    
    # Timestamp
    pdf.set_font('Korean', '', 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f'생성일시: {timestamp}', align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    
    # Line
    pdf.set_draw_color(100, 100, 100)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    # Patient info
    if patient_info:
        pdf.set_font('Korean', '', 14)
        pdf.cell(0, 10, '■ 환자 기본정보', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
        pdf.set_font('Korean', '', 10)
        
        info_items = [
            ('질환명', patient_info.get('disease', 'N/A')),
            ('변증/처방', patient_info.get('pattern', 'N/A')),
            ('나이/성별', f"{patient_info.get('age', 'N/A')}세 / {patient_info.get('sex', 'N/A')}"),
            ('신장/체중', f"{patient_info.get('height', 'N/A')}cm / {patient_info.get('weight', 'N/A')}kg"),
            ('활력징후', f"BP {patient_info.get('sbp', 'N/A')}/{patient_info.get('dbp', 'N/A')} mmHg, "
                      f"맥박 {patient_info.get('pulse_rate', 'N/A')}/분, "
                      f"체온 {patient_info.get('temp', 'N/A')}°C"),
        ]
        
        for label, value in info_items:
            pdf.cell(5, 7, '', new_x='RIGHT')  # Indent
            pdf.cell(35, 7, f'• {label}:', new_x='RIGHT')
            pdf.cell(0, 7, str(value), new_x='LMARGIN', new_y='NEXT')
        
        pdf.ln(8)
        pdf.set_draw_color(150, 150, 150)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(8)
    
    # Summary
    pdf.set_font('Korean', '', 14)
    pdf.cell(0, 10, '■ 요약', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)
    pdf.set_font('Korean', '', 10)
    pdf.multi_cell(0, 7, summary)
    pdf.ln(8)
    
    # Scenario - with improved section formatting
    pdf.set_draw_color(150, 150, 150)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    pdf.set_font('Korean', '', 14)
    pdf.cell(0, 10, '■ 환자 시나리오', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(5)
    pdf.set_font('Korean', '', 10)
    
    # Process scenario with improved formatting
    paragraphs = scenario.split('\n')
    for para in paragraphs:
        para = para.strip()
        if para:
            # Check if this is a section header (starts with 【 or [ or numbered section)
            if para.startswith('【') or para.startswith('[') or para.startswith('#'):
                pdf.ln(6)  # Extra space before section headers
                pdf.set_font('Korean', '', 12)
                pdf.multi_cell(0, 8, para)
                pdf.set_font('Korean', '', 10)
                pdf.ln(3)
            # Check if this is a bullet point item
            elif para.startswith('-') or para.startswith('•') or para.startswith('·'):
                pdf.cell(5, 7, '', new_x='RIGHT')  # Indent
                pdf.multi_cell(0, 7, para)
                pdf.ln(1)
            # Check if this is a sub-header or category
            elif ':' in para and len(para.split(':')[0]) < 20:
                pdf.set_font('Korean', '', 10)
                pdf.cell(5, 7, '', new_x='RIGHT')  # Small indent
                pdf.multi_cell(0, 7, para)
                pdf.ln(2)
            else:
                pdf.multi_cell(0, 7, para)
                pdf.ln(3)
    
    # Convert bytearray to bytes for Streamlit
    output = pdf.output()
    if isinstance(output, bytearray):
        return bytes(output)
    elif isinstance(output, bytes):
        return output
    else:
        return output.encode('latin-1') if isinstance(output, str) else bytes(output)

