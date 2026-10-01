import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 805, "YASSINE EL OUARDI — FEUILLE DE ROUTE STRATÉGIQUE & COMPÉTENCES D'AVENIR")
            self.drawRightString(A4[0] - 54, 805, "IBM i · MODERNISATION · AGENTS IA")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 798, A4[0] - 54, 798)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, A4[0] - 54, 45)
        self.drawString(54, 32, "Document Confidentiel & Stratégique · Ingénierie & Évolution Professionnelle")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(A4[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0f62fe") # IBM Blue
    dark_neutral = colors.HexColor("#0f172a")
    text_muted = colors.HexColor("#475569")
    accent_emerald = colors.HexColor("#059669")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=dark_neutral,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=primary_color,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=dark_neutral,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=primary_color,
        spaceBefore=6,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155")
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    mono_style = ParagraphStyle(
        'Mono_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # =========================================================================
    # PAGE 1: STRATEGIC VISION & ELITE POSITIONING
    # =========================================================================
    story.append(Paragraph("YASSINE EL OUARDI", ParagraphStyle('TopName', fontName='Helvetica-Bold', fontSize=10, textColor=primary_color)))
    story.append(Paragraph("Feuille de Route Stratégique : Compétences d'Avenir & Ingénierie d'Élite", title_style))
    story.append(Paragraph("De l'Analyste Développeur IBM i vers l'Architecte de Modernisation & Systèmes Agentiques", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0f62fe"), spaceAfter=14))

    # Executive Summary Card
    summary_text = (
        "<b>Synthèse Stratégique :</b> Les systèmes centraux (IBM i / AS400) traitent plus de 70% des transactions financières mondiales, "
        "mais font face à une pénurie critique d'ingénieurs capables de dialoguer simultanément avec les règles métiers historiques "
        "et les technologies de rupture (Next.js, APIs modernes, RAG et Agents Autonomes). Ce document définit votre trajectoire de positionnement "
        "dans le <b>top 0.1% des profils d'ingénierie</b> : allier la solidité absolue du transactionnel IBM i à la vélocité de l'intelligence artificielle agentique."
    )
    story.append(Table([[Paragraph(summary_text, body_style)]], colWidths=[A4[0]-108], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Le Diagnostic du Marché & Votre Avantage Compétitif", h1_style))
    
    diag_data = [
        [
            Paragraph("<b>Profil Développeur Classique</b>", body_bold),
            Paragraph("<b>Votre Profil Hybride d'Avenir</b>", body_bold)
        ],
        [
            Paragraph("• Maîtrise uniquement le web ou uniquement le legacy.<br/>• Ne comprend pas les contraintes comptables, paie ou fiscales.<br/>• Dépendant de prompts génériques produisant du code non vérifié.<br/>• Vulnérable à l'automatisation brute.", body_style),
            Paragraph("• <b>Pilier Métier :</b> Maîtrise prouvée des flux critiques (Finance, Paie, RAS, Budgets).<br/>• <b>Pilier Core :</b> RPG Free, SQLRPGLE, DB2 for i, intégrité transactionnelle.<br/>• <b>Pilier Modernisation :</b> Next.js, Node.js, Bun, architecture API REST/GraphQL.<br/>• <b>Pilier IA Agentique :</b> Orchestration d'agents (Dify, OpenHands, RAGFlow).", body_style)
        ]
    ]
    diag_table = Table(diag_data, colWidths=[(A4[0]-108)*0.45, (A4[0]-108)*0.55])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("2. La Matrice des 4 Piliers Technologiques", h1_style))

    piliers_data = [
        [Paragraph("<b>Pilier</b>", body_bold), Paragraph("<b>Technologies Clés (Sélectionnées)</b>", body_bold), Paragraph("<b>Objectif Stratégique pour Yassine</b>", body_bold)],
        [
            Paragraph("<b>1. Cœur IBM i & Données</b>", body_style),
            Paragraph("RPGLE, SQLRPGLE, RPG Free Format, DB2 for i, ILE, SQL Avancé.", mono_style),
            Paragraph("Garantir la sécurité, l'auditabilité et la performance des règles financières critiques.", body_style)
        ],
        [
            Paragraph("<b>2. Modernisation Web & API</b>", body_style),
            Paragraph("Next.js, React 19, Node.js Best Practices, Bun, pnpm, shadcn/ui, Vite.", mono_style),
            Paragraph("Transformer les écrans 5250 en portails web exécutifs ultra-rapides sans réécrire le cœur DB2.", body_style)
        ],
        [
            Paragraph("<b>3. IA Agentique & RAG</b>", body_style),
            Paragraph("OpenHands, Dify, RAGFlow, Crawlee, Google Gemini CLI, Agent Skills.", mono_style),
            Paragraph("Indexer la documentation légale/fiscale (RAG) et automatiser la refactorisation du code RPG.", body_style)
        ],
        [
            Paragraph("<b>4. Qualité & Design Goût</b>", body_style),
            Paragraph("Taste-Skill, Impeccable, Front-End-Checklist, Context-Mode, Superpowers.", mono_style),
            Paragraph("Éliminer tout 'AI Slop' : livrer des interfaces institutionnelles avec standard d'ingénierie suisse/IBM.", body_style)
        ],
    ]
    piliers_table = Table(piliers_data, colWidths=[(A4[0]-108)*0.25, (A4[0]-108)*0.40, (A4[0]-108)*0.35])
    piliers_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    for r in range(len(piliers_data)):
        piliers_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white)
        ]))
    story.append(piliers_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: IN-DEPTH BREAKDOWN OF CURATED REPOSITORIES & IMPACT
    # =========================================================================
    story.append(Paragraph("3. Analyse Approfondie des Compétences Sélectionnées", h1_style))
    story.append(Paragraph("Comment chaque brique open-source propulse directement votre valeur opérationnelle :", body_style))
    story.append(Spacer(1, 8))

    breakdown_data = [
        [
            Paragraph("<b>Catégorie</b>", body_bold),
            Paragraph("<b>Dépôt / Outil</b>", body_bold),
            Paragraph("<b>Application Directe dans Votre Quotidien & Évolution</b>", body_bold)
        ],
        # AI & Agents
        [
            Paragraph("<b>Agents Autonomes & Orchestration</b>", body_style),
            Paragraph("<b>OpenHands</b><br/><b>Dify</b><br/><b>msitarzewski/agency-agents</b>", mono_style),
            Paragraph("<b>Génération de tests et documentation automatique :</b> Déploiement d'agents capables d'analyser des programmes RPGLE existants, d'en extraire les règles comptables et de générer la spécification fonctionnelle sans perte de savoir.", body_style)
        ],
        [
            Paragraph("<b>RAG & Extraction de Données</b>", body_style),
            Paragraph("<b>infiniflow/ragflow</b><br/><b>firecrawl/firecrawl</b><br/><b>apify/crawlee</b>", mono_style),
            Paragraph("<b>Veille fiscale & budgétaire intelligente :</b> Indexer automatiquement les circulaires étatiques (ex: nouvelles réglementations RAS, circulaires budgétaires OFPPT) pour interroger directement le droit fiscal applicable aux tables DB2.", body_style)
        ],
        # Modern Web & Backend
        [
            Paragraph("<b>Backend & Intégration Robuste</b>", body_style),
            Paragraph("<b>goldbergyoni/nodebestpractices</b><br/><b>sindresorhus/awesome-nodejs</b><br/><b>oven-sh/bun</b>", mono_style),
            Paragraph("<b>Couche d'API moderne au-dessus de DB2 for i :</b> Architecture d'APIs micro-services sécurisées, scalables et testées unitairement, respectant les normes de résilience bancaire.", body_style)
        ],
        [
            Paragraph("<b>Frontend d'Entreprise & UI</b>", body_style),
            Paragraph("<b>vercel/next.js</b><br/><b>shadcn-ui/ui</b><br/><b>ant-design</b><br/><b>vitejs/vite</b>", mono_style),
            Paragraph("<b>Modernisation des écrans de gestion :</b> Remplacement des écrans verts 5250 par des tableaux de bord interactifs modernes pour les directeurs financiers et gestionnaires de paie.", body_style)
        ],
        # Taste & Craft
        [
            Paragraph("<b>Rigueur & Design d'Ingénieur</b>", body_style),
            Paragraph("<b>pbakaus/impeccable</b><br/><b>Leonxlnx/taste-skill</b><br/><b>thedaviddias/Front-End-Checklist</b>", mono_style),
            Paragraph("<b>Élimination de tout 'AI Slop' :</b> Garantir un niveau de finition digne d'IBM Carbon, avec accessibilité AA/AAA, performance Lighthouse 100/100 et zéro code superflu.", body_style)
        ],
        [
            Paragraph("<b>Productivité & Contexte LLM</b>", body_style),
            Paragraph("<b>mksglu/context-mode</b><br/><b>obra/superpowers</b><br/><b>google-gemini/gemini-cli</b>", mono_style),
            Paragraph("<b>Gestion de contexte complexe :</b> Permet de charger des schémas de bases de données relationnelles volumineux et des codes legacy dans le contexte des modèles sans hallucination.", body_style)
        ],
    ]

    breakdown_table = Table(breakdown_data, colWidths=[(A4[0]-108)*0.22, (A4[0]-108)*0.28, (A4[0]-108)*0.50])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("4. La Valeur Ajoutée pour Votre Portefeuille & Vos Recruteurs", h1_style))
    impact_box = (
        "<b>Ce que ce positionnement démontre à un recruteur / DSI :</b><br/>"
        "1. <b>Vous n'êtes pas un développeur AS400 enfermé dans le passé</b> : Vous apportez la modernité (React, Next.js, APIs modernes) au service des investissements existants.<br/>"
        "2. <b>Vous n'êtes pas un développeur web naïf</b> : Vous comprenez la criticité des données transactionnelles, les clôtures comptables, les enjeux de sécurité DB2 et la fiscalité réelle.<br/>"
        "3. <b>Vous êtes à la pointe de l'ingénierie IA</b> : Vous savez utiliser les agents pour auditer, sécuriser et accélérer la maintenance applicative."
    )
    story.append(Table([[Paragraph(impact_box, body_style)]], colWidths=[A4[0]-108], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3b82f6")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CONCRETE 3-HORIZON ACTION PLAN
    # =========================================================================
    story.append(Paragraph("5. Plan d'Action Opérationnel par Horizons", h1_style))
    story.append(Paragraph("Étapes chronologiques pour matérialiser cette montée en puissance :", body_style))
    story.append(Spacer(1, 8))

    plan_data = [
        [
            Paragraph("<b>Horizon Temporel</b>", body_bold),
            Paragraph("<b>Objectifs Techniques Concrets</b>", body_bold),
            Paragraph("<b>Livrable Démonstrateur (Pour le Portfolio)</b>", body_bold)
        ],
        [
            Paragraph("<b>HORIZON 1<br/>(0 à 6 mois)<br/>Fondation & Bridge</b>", body_style),
            Paragraph("• Consolidation RPG Free modulaire & Procédures SQLRPGLE.<br/>• Exposition d'APIs REST Node.js / Bun connectées à DB2 for i.<br/>• Mise en place de règles de code strictes (Node Best Practices, Front-End-Checklist).<br/>• Veille active via RAG sur les textes légaux (RAS, TVA).", body_style),
            Paragraph("<b>Cas d'étude publié :</b> 'API Gateway moderne Node.js pour transactions DB2 for i avec authentification JWT et monitoring'.", body_style)
        ],
        [
            Paragraph("<b>HORIZON 2<br/>(6 à 18 mois)<br/>Modernisation Complète</b>", body_style),
            Paragraph("• Développement de micro-frontends Next.js / shadcn-ui pour modules de gestion (ex: consultation des situations budgétaires).<br/>• Intégration de pipelines CI/CD et conteneurisation (Docker, Cloud SAAICC).<br/>• Utilisation d'agents Dify pour assister l'analyse des incidents de production.", body_style),
            Paragraph("<b>Démonstrateur Interactif :</b> 'Dashboard Financier exécutif Next.js connecté en temps réel aux données de paie et trésorerie'.", body_style)
        ],
        [
            Paragraph("<b>HORIZON 3<br/>(18 à 36 mois)<br/>Architecte Hybride</b>", body_style),
            Paragraph("• Pilotage de projets de refonte ou cohabitation Legacy / Cloud.<br/>• Déploiement de systèmes agentiques d'entreprise (OpenHands / RAGFlow) pour l'audit automatique du patrimoine applicatif.<br/>• Positionnement comme <b>Référent Technique Grands Comptes</b> (Banques, Assurances, Groupes Industriels).", body_style),
            Paragraph("<b>Livre blanc / Conférence :</b> 'Stratégie de modernisation pérenne des ERP IBM i sans rupture transactionnelle'.", body_style)
        ],
    ]

    plan_table = Table(plan_data, colWidths=[(A4[0]-108)*0.22, (A4[0]-108)*0.45, (A4[0]-108)*0.33])
    plan_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(plan_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph("6. Engagement & Signature Professionnelle", h1_style))
    sign_box = (
        "<b>Synthèse Finale :</b> La rareté de votre double compétence (Finance critique + IBM i + IA / Modern Web) constitue votre "
        "plus fort levier de valorisation salariale et de choix de carrière. En appliquant la rigueur d'ingénierie documentée ici, "
        "vous consolidez un profil d'exception, immédiatement crédible auprès des comités de direction et directions techniques.<br/><br/>"
        "<b>Document établi pour :</b> Yassine EL OUARDI<br/>"
        "<b>Coordonnées :</b> elouardii.yassine@gmail.com · +212 6 17 20 71 46 · Casablanca, Maroc"
    )
    story.append(Table([[Paragraph(sign_box, body_style)]], colWidths=[A4[0]-108], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == '__main__':
    target = os.path.join(r"H:\Mon Drive\Perso\Portfolio", "ROADMAP_STRATEGIQUE_SKILLS_YASSINE_EL_OUARDI.pdf")
    build_pdf(target)
