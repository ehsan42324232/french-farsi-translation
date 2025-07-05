#!/usr/bin/env python3
"""
Complete Professional French to Farsi Translation System - Part 2
Continuation of the comprehensive translation tool
"""

        sentences = re.split(r'[.!?]+', current_chunk)
                current_sentences = []
                temp_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(temp_chunk + sentence) <= max_chars:
                        temp_chunk += sentence + ". "
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + ". "
                
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
                    
                current_chunk = paragraph + "\n\n"
            else:
                current_chunk += paragraph + "\n\n"
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def enhance_translation(self, french_text: str, google_translation: str) -> str:
        """
        Enhance Google Translate output with custom dictionary and corrections.
        """
        enhanced = google_translation
        
        # Apply custom dictionary corrections
        for french_phrase, farsi_phrase in self.enhanced_dictionary.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(french_phrase) + r'\b'
            enhanced = re.sub(pattern, farsi_phrase, enhanced, flags=re.IGNORECASE)
        
        # Post-processing corrections for common translation errors
        corrections = {
            # Fix common Google Translate issues with Persian
            "در آن": "آن",
            "بود که": "که",
            "در این": "این",
            "است که": "که",
            "می شود": "می‌شود",
            "نمی توان": "نمی‌توان",
            "می تواند": "می‌تواند",
            "خواهد بود": "خواهد بود",
            "خواهد شد": "خواهد شد",
        }
        
        for incorrect, correct in corrections.items():
            enhanced = enhanced.replace(incorrect, correct)
        
        return enhanced
    
    def translate_chunk(self, text_chunk: str, chunk_number: int, total_chunks: int) -> str:
        """
        Translate a single chunk of text with progress tracking.
        """
        if self.progress_callback:
            self.progress_callback(chunk_number, total_chunks, f"Translating chunk {chunk_number}")
        
        # Check cache first
        cache_key = hash(text_chunk)
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        try:
            if self.translator:
                # Use Google Translate
                time.sleep(1)  # Rate limiting
                result = self.translator.translate(text_chunk, src='fr', dest='fa')
                base_translation = result.text if result else text_chunk
            else:
                # Fallback to dictionary-only translation
                base_translation = self.dictionary_translate(text_chunk)
            
            # Enhance with custom dictionary
            enhanced_translation = self.enhance_translation(text_chunk, base_translation)
            
            # Cache the result
            self.translation_cache[cache_key] = enhanced_translation
            
            return enhanced_translation
            
        except Exception as e:
            print(f"⚠️ Translation error for chunk {chunk_number}: {e}")
            # Fallback to basic dictionary translation
            return self.dictionary_translate(text_chunk)
    
    def dictionary_translate(self, text: str) -> str:
        """
        Fallback translation using only the custom dictionary.
        """
        translated = text.lower()
        
        # Apply dictionary translations
        for french, farsi in self.enhanced_dictionary.items():
            pattern = r'\b' + re.escape(french) + r'\b'
            translated = re.sub(pattern, farsi, translated, flags=re.IGNORECASE)
        
        return translated
    
    def create_professional_word_document(self, 
                                        original_chunks: List[str], 
                                        translated_chunks: List[str],
                                        include_original: bool = True) -> Document:
        """
        Create a professional Word document with proper Farsi formatting.
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx is required. Install with: pip install python-docx")
        
        doc = Document()
        
        # Set up document properties
        doc.core_properties.title = "ترجمه کامل از فرانسه به فارسی"
        doc.core_properties.author = "AI Translation System"
        doc.core_properties.subject = "Complete French to Farsi Translation"
        doc.core_properties.keywords = "French, Farsi, Persian, Translation"
        
        # Create styles
        self._create_document_styles(doc)
        
        # Document header
        title = doc.add_heading('ترجمه کامل از فرانسه به فارسی', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._set_rtl_paragraph(title)
        
        subtitle = doc.add_heading('Complete French to Farsi Translation', 1)
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Metadata section
        doc.add_paragraph()
        metadata = doc.add_paragraph()
        metadata.add_run('تاریخ ترجمه: ').bold = True
        metadata.add_run(datetime.now().strftime('%Y/%m/%d'))
        metadata.add_run('\nتعداد بخش‌ها: ').bold = True
        metadata.add_run(str(len(translated_chunks)))
        metadata.add_run('\nفایل اصلی: ').bold = True
        metadata.add_run('1-4.txt')
        metadata.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._set_rtl_paragraph(metadata)
        
        # Add decorative separator
        separator = doc.add_paragraph('═' * 60)
        separator.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Table of contents placeholder
        toc_heading = doc.add_heading('فهرست مطالب', 2)
        toc_heading.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._set_rtl_paragraph(toc_heading)
        
        toc = doc.add_paragraph()
        for i in range(len(translated_chunks)):
            toc.add_run(f'بخش {i+1}')
            toc.add_run('\t' + '.' * 50 + f'\t{i+1}\n')
        toc.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        self._set_rtl_paragraph(toc)
        
        # Page break
        doc.add_page_break()
        
        # Process each chunk
        for i, (original_chunk, translated_chunk) in enumerate(zip(original_chunks, translated_chunks), 1):
            # Section header
            section_header = doc.add_heading(f'بخش {i}', 2)
            section_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            self._set_rtl_paragraph(section_header)
            
            if include_original:
                # Original French text
                french_label = doc.add_paragraph()
                french_run = french_label.add_run('متن اصلی (فرانسه):')
                french_run.bold = True
                french_run.font.color.rgb = RGBColor(0, 0, 139)  # Dark blue
                french_label.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                self._set_rtl_paragraph(french_label)
                
                french_text = doc.add_paragraph(original_chunk)
                french_text.alignment = WD_ALIGN_PARAGRAPH.LEFT
                french_text.style = 'French Text'
                
                # Add spacing
                doc.add_paragraph()
            
            # Translated Farsi text
            farsi_label = doc.add_paragraph()
            farsi_run = farsi_label.add_run('ترجمه (فارسی):')
            farsi_run.bold = True
            farsi_run.font.color.rgb = RGBColor(139, 0, 0)  # Dark red
            farsi_label.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            self._set_rtl_paragraph(farsi_label)
            
            farsi_text = doc.add_paragraph(translated_chunk)
            farsi_text.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            farsi_text.style = 'Farsi Text'
            self._set_rtl_paragraph(farsi_text)
            
            # Add separator between sections (except for the last one)
            if i < len(translated_chunks):
                separator = doc.add_paragraph('─' * 50)
                separator.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph()  # Extra spacing
        
        return doc
    
    def _create_document_styles(self, doc: Document):
        """Create custom styles for the document."""
        styles = doc.styles
        
        # Farsi text style
        try:
            farsi_style = styles.add_style('Farsi Text', WD_STYLE_TYPE.PARAGRAPH)
            farsi_style.font.name = 'B Nazanin'
            farsi_style.font.size = Pt(14)
            farsi_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            farsi_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            farsi_style.paragraph_format.space_after = Pt(6)
        except ValueError:
            pass  # Style already exists
        
        # French text style
        try:
            french_style = styles.add_style('French Text', WD_STYLE_TYPE.PARAGRAPH)
            french_style.font.name = 'Times New Roman'
            french_style.font.size = Pt(12)
            french_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            french_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            french_style.paragraph_format.space_after = Pt(6)
        except ValueError:
            pass  # Style already exists
    
    def _set_rtl_paragraph(self, paragraph):
        """Set Right-to-Left direction for Farsi text."""
        try:
            pPr = paragraph._element.get_or_add_pPr()
            bidi = OxmlElement('w:bidi')
            bidi.set(qn('w:val'), '1')
            pPr.append(bidi)
        except Exception as e:
            print(f"⚠️ RTL setup warning: {e}")
    
    def translate_large_file(self, 
                           file_path: str, 
                           output_filename: str = None,
                           include_original: bool = True,
                           chunk_size: int = 3000) -> str:
        """
        Main function to translate a large French file to Farsi.
        """
        print("🚀 Starting Professional French to Farsi Translation System")
        print("=" * 60)
        
        # Read the file
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"📖 Reading file: {file_path.name}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_size_mb = len(content) / (1024 * 1024)
        print(f"📏 File size: {file_size_mb:.2f} MB ({len(content):,} characters)")
        
        # Split into chunks
        print(f"✂️ Splitting text into chunks (max {chunk_size} chars each)...")
        chunks = self.split_text_intelligently(content, chunk_size)
        print(f"📦 Created {len(chunks)} chunks for translation")
        
        # Progress tracking
        def progress_callback(current, total, message):
            progress = (current / total) * 100
            print(f"⏳ {message} - Progress: {progress:.1f}% ({current}/{total})")
        
        self.set_progress_callback(progress_callback)
        
        # Translate each chunk
        print(f"\n🔄 Starting translation process...")
        translated_chunks = []
        
        for i, chunk in enumerate(chunks, 1):
            translated = self.translate_chunk(chunk, i, len(chunks))
            translated_chunks.append(translated)
            
            # Show sample from first chunk
            if i == 1:
                sample_length = min(100, len(chunk))
                print(f"\n📝 Sample from first chunk:")
                print(f"   French: {chunk[:sample_length]}...")
                print(f"   Farsi:  {translated[:sample_length]}...")
        
        # Create Word document
        print(f"\n📄 Creating professional Word document...")
        doc = self.create_professional_word_document(chunks, translated_chunks, include_original)
        
        # Save document
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"french_farsi_translation_{timestamp}.docx"
        
        output_path = self.output_dir / output_filename
        doc.save(output_path)
        
        # Summary
        print(f"\n✅ Translation completed successfully!")
        print(f"📁 Output saved to: {output_path}")
        print(f"📊 Translation Statistics:")
        print(f"   • Original text: {len(content):,} characters")
        print(f"   • Number of chunks: {len(chunks)}")
        print(f"   • Translation method: {'Google Translate + Custom Dictionary' if self.translator else 'Custom Dictionary Only'}")
        print(f"   • Include original: {'Yes' if include_original else 'No'}")
        print(f"   • Processing time: {time.time():.1f} seconds")
        
        return str(output_path)

def main():
    """
    Main function to demonstrate the translation system.
    """
    print("🌟 Professional French to Farsi Translation System")
    print("🔧 Version 2.0 - Enhanced with comprehensive dictionary")
    print("=" * 60)
    
    # Initialize translator
    translator = ProfessionalFrenchFarsiTranslator()
    
    # Check dependencies
    missing_deps = []
    if not DOCX_AVAILABLE:
        missing_deps.append("python-docx")
    if not TRANSLATOR_AVAILABLE:
        missing_deps.append("googletrans==4.0.0rc1")
    
    if missing_deps:
        print("⚠️ Missing dependencies:")
        for dep in missing_deps:
            print(f"   pip install {dep}")
        print("\nInstall missing dependencies and run again.")
        return
    
    # Sample text for demonstration
    sample_french_text = """
    Bonjour et bienvenue dans ce système de traduction professionnel.
    
    Cette application traduit automatiquement de longs textes français vers le farsi (persan) 
    en utilisant une combinaison de Google Translate et d'un dictionnaire personnalisé 
    contenant plus de 500 expressions françaises courantes.
    
    Le système divise intelligemment le texte en segments pour préserver la structure 
    des phrases et des paragraphes, puis génère un document Word professionnel avec 
    un formatage RTL (droite à gauche) approprié pour le texte farsi.
    
    Merci d'utiliser notre système de traduction. Nous espérons qu'il vous sera utile 
    pour vos projets de traduction français-farsi.
    """
    
    print("\n📝 Demonstration with sample text:")
    print("-" * 40)
    
    # Create temporary file for demonstration
    sample_file = Path("sample_french.txt")
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_french_text)
    
    try:
        # Translate the sample
        output_file = translator.translate_large_file(
            str(sample_file),
            "sample_translation.docx",
            include_original=True,
            chunk_size=500  # Small chunks for demo
        )
        
        print(f"\n🎉 Demonstration completed!")
        print(f"📄 Sample translation saved as: {output_file}")
        print(f"\n💡 To translate your 1-4.txt file:")
        print(f"   translator.translate_large_file('1-4.txt', 'complete_translation.docx')")
        
    finally:
        # Clean up
        if sample_file.exists():
            sample_file.unlink()

if __name__ == "__main__":
    main()
