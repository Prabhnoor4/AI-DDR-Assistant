# pdf download

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import re


class PDFRenderer:
    #converts markdown to pdf
    
    @staticmethod
    def render(markdown_content: str, output_path: str) -> str:
        #returns pdf file path
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=20,
            leftIndent=0,
            borderColor=colors.HexColor('#3498db'),
            borderWidth=0,
            borderPadding=5
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        bold_style = ParagraphStyle(
            'CustomBold',
            parent=body_style,
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica-Bold'
        )
        
        # Parse markdown and convert to PDF elements
        lines = markdown_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Title (# )
            if line.startswith('# '):
                title_text = line[2:].strip()
                story.append(Paragraph(title_text, title_style))
                story.append(Spacer(1, 0.2*inch))
            
            # Heading (## )
            elif line.startswith('## '):
                heading_text = line[3:].strip()
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph(heading_text, heading_style))
                story.append(Spacer(1, 0.1*inch))
            
            # Bold text (**text**)
            elif line.startswith('**') and line.endswith('**'):
                bold_text = line[2:-2]
                story.append(Paragraph(f"<b>{bold_text}</b>", body_style))
            
            # Horizontal rule (---)
            elif line.startswith('---'):
                story.append(Spacer(1, 0.1*inch))
                # Add a thin line
                from reportlab.platypus import HRFlowable
                story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
                story.append(Spacer(1, 0.1*inch))
            
            # Bullet list (- )
            elif line.startswith('- '):
                bullet_text = line[2:].strip()
                # Handle bold within bullets
                bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', bullet_text)
                story.append(Paragraph(f"• {bullet_text}", body_style))
            
            # Numbered list (1. )
            elif re.match(r'^\d+\.\s', line):
                list_text = re.sub(r'^\d+\.\s', '', line)
                list_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', list_text)
                story.append(Paragraph(list_text, body_style))
            
            # Regular paragraph
            else:
                # Handle bold and italic
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                story.append(Paragraph(text, body_style))
            
            i += 1
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    @staticmethod
    def render_from_file(markdown_file: str, output_file: str = None) -> str:
        
        from pathlib import Path
        
        # reading markdown content
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # generates output filename if not provided
        if output_file is None:
            md_path = Path(markdown_file)
            output_file = str(md_path.with_suffix('.pdf'))
        
        return PDFRenderer.render(markdown_content, output_file)
