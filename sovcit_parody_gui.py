import tkinter as tk
from tkinter import ttk, messagebox
import difflib
import random
import re
from collections import Counter

APP_TITLE = "SovCit Claim vs Reality"
APP_GEOMETRY = "1480x860"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "at", "by", "with",
    "about", "from", "is", "are", "was", "were", "be", "been", "being", "that", "this",
    "it", "as", "into", "their", "there", "they", "them", "you", "your", "my", "our",
    "we", "i", "me", "do", "does", "did", "can", "could", "would", "should", "have",
    "has", "had", "not", "but", "if", "then", "than", "so", "such", "just", "up", "out",
    "over", "under", "because", "when", "where", "why", "how", "what", "which", "who"
}

TOPICS = [
    {
        "title": "Right to Travel",
        "aliases": [
            "traveling not driving",
            "right to travel",
            "free movement",
            "license for travel",
            "driver license not required",
            "travel argument"
        ],
        "tags": [
            "travel", "driving", "license", "driver", "vehicle", "conveyance", "commercial", "motor vehicle"
        ],
        "sovcit_claim": (
            "I am not engaged in commerce. I am traveling in my private conveyance under the God-given right to locomotion. "
            "A driver license is only required for those operating in commercial enterprise. I am not driving. I am traveling."
        ),
        "sovcit_explanation": (
            "This argument tries to split ordinary vehicle use into two separate worlds: 'driving' for commerce and 'traveling' for everyone else. "
            "In sovereign-citizen framing, the person claims they have transformed a car into a private conveyance by declaration alone, "
            "which they believe places them outside normal licensing, registration, and insurance laws."
        ),
        "flaw_summary": (
            "The right to travel does exist in a broad constitutional sense, but it does not erase the state's ability to regulate how motor vehicles are operated on public roads."
        ),
        "legal_reality": (
            "Courts generally recognize freedom of movement, including the ability to move from place to place and between states without improper government interference. "
            "That does not create an unrestricted right to operate a motor vehicle without a license, registration, or insurance. Walking is one thing. Operating a machine on shared public roads is another, and states may regulate that for public safety."
        ),
        "court_reality": (
            "Judges reject this because the argument confuses a protected liberty interest in movement with immunity from traffic laws. A person may have a right to go somewhere, but not an absolute right to use any method they want without regulation."
        ),
        "judicial_pushback": (
            "Typical bench response: yes, you can travel. On your feet. The existence of a liberty interest in movement does not nullify licensing rules for motor vehicles."
        ),
        "semantic_trick": (
            "Common word game: redefining 'drive' as commercial-only while pretending 'travel' is a separate legal shield word."
        ),
        "parody_citation": "Claimed authority stack: Magna Carta + Black's Law Dictionary + vibes + a laminated printout from 2009."
    },
    {
        "title": "Strawman / ALL CAPS Name Theory",
        "aliases": [
            "strawman",
            "all caps name",
            "corporate fiction",
            "legal fiction",
            "birth certificate person",
            "name entity"
        ],
        "tags": [
            "strawman", "caps", "name", "birth certificate", "entity", "corporation", "legal fiction"
        ],
        "sovcit_claim": (
            "The ALL-CAPS name is a corporate fiction created by the state. That entity is not me. I appear by special visitation as the living man, not the artificial person."
        ),
        "sovcit_explanation": (
            "This claim tries to split one human being into two separate legal beings: the living person and a government-created paper avatar. "
            "The sovereign-citizen script then argues that debts, court authority, taxes, and criminal liability attach only to the paper avatar."
        ),
        "flaw_summary": (
            "Capitalization style in legal documents does not create a second legal being and does not sever the person from their obligations or identity in court."
        ),
        "legal_reality": (
            "Names are often formatted in capitals for consistency in databases, forms, and records. That formatting has no power to create a separate corporate shell person immune from law. Courts treat this theory as pseudo-legal nonsense."
        ),
        "court_reality": (
            "Judges reject it because it has no basis in actual law. The person standing in court is still the person named in the case, regardless of typography."
        ),
        "judicial_pushback": (
            "Typical bench response: the caption style on a document is not a jurisdictional escape hatch. You are still the person before the court."
        ),
        "semantic_trick": (
            "Common word game: treating capitalization, punctuation, or spacing as if grammar creates a separate legal species."
        ),
        "parody_citation": "Claimed authority stack: birth certificate numerology + dictionary mining + one guy on YouTube in wraparound sunglasses."
    },
    {
        "title": "UCC Filing / Secret Treasury Account",
        "aliases": [
            "ucc 1",
            "ucc financing statement",
            "redemption theory",
            "secret account",
            "treasury account",
            "birth certificate account"
        ],
        "tags": [
            "ucc", "treasury", "account", "redemption", "finance", "birth certificate", "security interest"
        ],
        "sovcit_claim": (
            "By filing the proper UCC paperwork, I secure my interest in the strawman and gain access to the value attached to my birth certificate trust account."
        ),
        "sovcit_explanation": (
            "This argument borrows commercial filing language and tries to convert it into a hidden wealth ritual. The idea is that a secret account exists, "
            "and the right paperwork somehow releases it or lets the filer control the legal fiction tied to their name."
        ),
        "flaw_summary": (
            "The Uniform Commercial Code governs certain commercial transactions. It does not create hidden citizen accounts or let people opt out of law through filing tricks."
        ),
        "legal_reality": (
            "A UCC filing is generally a notice mechanism related to secured transactions. It is not a spell, not a citizenship override, and not a key to a secret treasury fund. Courts and agencies reject these claims."
        ),
        "court_reality": (
            "Judges reject it because the filing has nothing to do with criminal jurisdiction, taxes, license requirements, or imaginary trust accounts."
        ),
        "judicial_pushback": (
            "Typical bench response: filing unrelated commercial paperwork does not alter criminal, civil, or traffic obligations."
        ),
        "semantic_trick": (
            "Common word game: importing technical commercial terms into unrelated legal settings and pretending the jargon itself carries authority."
        ),
        "parody_citation": "Claimed authority stack: UCC-1, red ink thumbprint, notary seal, and hidden gold allegedly stored in the moon."
    },
    {
        "title": "Maritime / Admiralty Law in Ordinary Court",
        "aliases": [
            "maritime law",
            "admiralty law",
            "yellow fringe flag",
            "court is admiralty",
            "landlocked admiralty",
            "captain of the vessel"
        ],
        "tags": [
            "maritime", "admiralty", "flag", "fringe", "courtroom", "jurisdiction", "vessel"
        ],
        "sovcit_claim": (
            "This is an admiralty court operating under maritime jurisdiction, proven by the fringed flag and the fact that the court treats my body as a vessel in commerce."
        ),
        "sovcit_explanation": (
            "This argument tries to turn visual symbols, wordplay, and nautical metaphors into jurisdictional proof. "
            "It often appears in traffic or criminal hearings where the person insists the courtroom is secretly operating under sea law despite being nowhere near the ocean."
        ),
        "flaw_summary": (
            "A decorative flag fringe does not transform a state or local courtroom into a maritime court, and wordplay about 'vessels' has no controlling legal force."
        ),
        "legal_reality": (
            "Ordinary state courts handle state matters under normal statutory and constitutional law. Admiralty jurisdiction applies to specific maritime matters, not routine criminal or traffic cases in Kansas, Oklahoma, or anywhere else inland by rhetorical pirate magic."
        ),
        "court_reality": (
            "Judges reject this because courtroom décor is not jurisdiction, and maritime law is a specialized legal field with an actual subject matter."
        ),
        "judicial_pushback": (
            "Typical bench response: this is not an admiralty proceeding, the fringe on a flag is decorative, and we are plainly not hearing a ship-collision case in a traffic courtroom."
        ),
        "semantic_trick": (
            "Common word game: grabbing words like vessel, dock, berth, captain, and person and pretending metaphor equals jurisdiction."
        ),
        "parody_citation": "Claimed authority stack: yellow fringe on flag + dictionary entry for 'vessel' + a mental image of a schooner parked outside the courthouse."
    },
    {
        "title": "No Consent = No Jurisdiction",
        "aliases": [
            "i do not consent",
            "no jurisdiction",
            "consent required",
            "refuse contract",
            "court has no authority",
            "special appearance"
        ],
        "tags": [
            "consent", "jurisdiction", "contract", "court", "authority", "appearance"
        ],
        "sovcit_claim": (
            "I do not consent to these proceedings and therefore this court lacks jurisdiction over my person. I am here under threat, duress, and coercion."
        ),
        "sovcit_explanation": (
            "This argument treats government authority like a private contract that becomes invalid if one party refuses to sign or verbally objects. "
            "The speaker assumes that saying the right refusal phrase cancels the court's power."
        ),
        "flaw_summary": (
            "Jurisdiction in criminal and traffic matters does not depend on a defendant's personal consent in the same way a private contract would."
        ),
        "legal_reality": (
            "Courts derive jurisdiction from constitutions, statutes, subject matter, territory, and proper procedure. A defendant cannot usually dissolve that authority by declaring non-consent."
        ),
        "court_reality": (
            "Judges reject this because otherwise every defendant could escape process by simply refusing to participate. Legal systems do not work as optional subscription services."
        ),
        "judicial_pushback": (
            "Typical bench response: your consent is not what gives this court subject-matter jurisdiction over the case before it."
        ),
        "semantic_trick": (
            "Common word game: treating public law like a private contract and using refusal language as if government power were a click-wrap agreement."
        ),
        "parody_citation": "Claimed authority stack: contract law remix + volume turned up to maximum + three repetitions of 'I do not consent.'"
    },
    {
        "title": "Common Law Overrides Statutory Law",
        "aliases": [
            "common law only",
            "I stand on common law",
            "statutory law not valid",
            "natural law only",
            "common law court"
        ],
        "tags": [
            "common law", "statutory law", "natural law", "court", "constitution"
        ],
        "sovcit_claim": (
            "I stand under common law and natural law. Statutory codes only bind corporate persons, agents, and those who contract into them."
        ),
        "sovcit_explanation": (
            "This argument elevates vague historical notions of common law into a universal override system. "
            "The speaker treats statutes as optional corporate policies rather than law enacted through recognized legislative authority."
        ),
        "flaw_summary": (
            "Common law and statutory law coexist. Statutes are real law, and courts routinely apply them to actual people."
        ),
        "legal_reality": (
            "In modern legal systems, legislatures pass statutes and courts interpret and apply them. Common law does not automatically erase enacted law just because someone prefers older or more romantic-sounding terminology."
        ),
        "court_reality": (
            "Judges reject this because personal preference for 'common law' does not cancel statutes that validly govern conduct."
        ),
        "judicial_pushback": (
            "Typical bench response: statutes enacted by the proper legislative body are law, whether or not you approve of them."
        ),
        "semantic_trick": (
            "Common word game: using 'natural law' or 'common law' as grand-sounding override phrases with no actual mechanism for voiding statutes."
        ),
        "parody_citation": "Claimed authority stack: medieval mood board + selective history + refusal to accept the invention of legislatures."
    },
    {
        "title": "Refusing Name / Personhood Questions",
        "aliases": [
            "I am not a person",
            "person means corporation",
            "name refusal",
            "do not identify",
            "who is the defendant",
            "personhood trick",
            "living man",
            "living woman",
            "living person"
        ],
        "tags": [
            "person", "name", "identity", "defendant", "legal definition", "refusal", "living person"
        ],
        "sovcit_claim": (
            "I am not a person as defined by your statutes. I am a living man, a living woman, a living soul. I will not identify as the defendant or answer to the legal fiction attached to that label."
        ),
        "sovcit_explanation": (
            "This argument tries to exploit narrow or context-specific legal definitions by pretending a definition from one area of law cancels ordinary identity in another. "
            "It often comes with evasive answers about names, personhood, and standing, plus repeated emphasis on being 'alive' as if the court thought otherwise."
        ),
        "flaw_summary": (
            "Legal definitions are context-specific. Pulling one definition out of context does not erase ordinary legal identity in a courtroom. Being a 'living person' is not a defense category."
        ),
        "legal_reality": (
            "Courts identify parties based on the case, charging instruments, records, and the actual person present. Semantic games over the word 'person' do not immunize someone from proceedings. Saying 'I am a living person' does not place a human being outside the law that applies to human beings."
        ),
        "court_reality": (
            "Judges reject this because law is not interpreted by isolated dictionary scavenger hunts detached from context. The court already understands that the defendant is a living human being."
        ),
        "judicial_pushback": (
            "Typical bench response: yes, you are a living person. That does not deprive the court of jurisdiction or eliminate the charges."
        ),
        "semantic_trick": (
            "Common word game: trying to weaponize the word person, then switching to living man or living woman as if biology defeats procedure."
        ),
        "parody_citation": "Claimed authority stack: one clipped definition + dramatic pause + refusal to answer simple questions until everyone is exhausted."
    },
    {
        "title": "Taxes Are Voluntary",
        "aliases": [
            "income tax voluntary",
            "tax not mandatory",
            "no duty to file",
            "IRS has no authority",
            "voluntary compliance"
        ],
        "tags": [
            "tax", "irs", "income tax", "filing", "voluntary compliance", "federal"
        ],
        "sovcit_claim": (
            "The income tax system is voluntary, and without my consent or contract there is no lawful duty for me to file or pay."
        ),
        "sovcit_explanation": (
            "This argument usually misreads the phrase 'voluntary compliance' and treats it as proof that tax obligations are optional. "
            "In sovereign-citizen phrasing, the filing system is reframed as a consent trap rather than a legal obligation."
        ),
        "flaw_summary": (
            "'Voluntary compliance' refers to the system relying on taxpayers to accurately self-report in the first instance, not to taxes being optional."
        ),
        "legal_reality": (
            "Tax obligations arise from law, not private contract. Courts repeatedly reject arguments that federal income tax is optional for people who meet filing and payment requirements."
        ),
        "court_reality": (
            "Judges reject this because the law imposes duties whether or not the taxpayer likes them."
        ),
        "judicial_pushback": (
            "Typical bench response: voluntary compliance does not mean voluntary liability."
        ),
        "semantic_trick": (
            "Common word game: stripping a phrase from administrative context and pretending it means the entire tax system is elective."
        ),
        "parody_citation": "Claimed authority stack: one IRS phrase stripped of context + enormous confidence + an impending lien."
    },
    {
        "title": "License Plates / Registration Are Unnecessary for Private Use",
        "aliases": [
            "no registration needed",
            "private plate",
            "private conveyance plate",
            "traveler plate",
            "plate not required"
        ],
        "tags": [
            "registration", "plates", "private use", "vehicle", "road", "traveler"
        ],
        "sovcit_claim": (
            "Because my conveyance is privately owned and not used in commerce, registration and state-issued plates are not required."
        ),
        "sovcit_explanation": (
            "This argument extends the travel-not-driving theory into registration law, often accompanied by homemade tags and disclaimers. "
            "The claim is that private ownership somehow dissolves state authority over public-road use."
        ),
        "flaw_summary": (
            "Private ownership of a vehicle does not erase the state's power to regulate its use on public roads."
        ),
        "legal_reality": (
            "Registration and plate requirements are generally tied to operating a vehicle on public roadways, not to whether the vehicle owner considers themselves a merchant. Homemade 'private traveler' tags do not replace valid registration."
        ),
        "court_reality": (
            "Judges reject this because the public road system is regulated, and personal declarations do not substitute for legal compliance."
        ),
        "judicial_pushback": (
            "Typical bench response: the fact that you privately own the car does not make state registration laws disappear when you use public roads."
        ),
        "semantic_trick": (
            "Common word game: blending private property rights with public-road immunity as though ownership erases regulation."
        ),
        "parody_citation": "Claimed authority stack: printer paper plate + bold black marker + complete faith in the phrase 'private conveyance.'"
    },
    {
        "title": "Police / Courts Need an Injured Party",
        "aliases": [
            "where is the injured party",
            "no victim no crime",
            "victimless crime invalid",
            "who was harmed",
            "damaged party"
        ],
        "tags": [
            "victim", "injured party", "crime", "traffic", "state", "harm"
        ],
        "sovcit_claim": (
            "There is no injured party before this court, therefore there is no valid cause of action and no crime."
        ),
        "sovcit_explanation": (
            "This argument assumes every offense must look like a private lawsuit for direct damages between two individuals. "
            "It ignores public-order offenses and the state's role in prosecuting violations of law."
        ),
        "flaw_summary": (
            "Not every criminal or regulatory offense requires a separately identified individual victim in the way a civil damages case might."
        ),
        "legal_reality": (
            "States may criminalize conduct that harms public safety, public order, or regulatory interests. Traffic offenses, licensing violations, and many criminal statutes can be enforced without a specific person appearing as the injured plaintiff."
        ),
        "court_reality": (
            "Judges reject this because criminal law is not limited to one-on-one injury claims."
        ),
        "judicial_pushback": (
            "Typical bench response: the state may prosecute offenses against public order and safety even when there is no separate complainant standing in front of you."
        ),
        "semantic_trick": (
            "Common word game: trying to force criminal enforcement into the mold of a private civil dispute."
        ),
        "parody_citation": "Claimed authority stack: civil lawsuit logic jammed into criminal court with the confidence of a man who printed his own business cards."
    },
    {
        "title": "Represent vs Re-Present / Understand vs Under-Stand",
        "aliases": [
            "represent re present",
            "understand under stand",
            "I do not stand under",
            "semantic trick words",
            "word splitting",
            "etymology defense"
        ],
        "tags": [
            "represent", "understand", "under stand", "re present", "semantics", "wordplay", "grammar"
        ],
        "sovcit_claim": (
            "I cannot re-present anyone because that would mean to present them again. I do not understand, because I do not stand under anything. These are trick words intended to bind me through linguistic fraud."
        ),
        "sovcit_explanation": (
            "This is one of the purest forms of sovereign-citizen word magic. Ordinary legal and conversational terms are chopped into smaller pieces, then redefined according to literal syllables rather than actual usage, legal context, or common meaning."
        ),
        "flaw_summary": (
            "Courts do not interpret ordinary language by letting litigants invent brand-new meanings from syllable fragments. Word-splitting is not legal analysis."
        ),
        "legal_reality": (
            "In ordinary English and legal usage, represent means to act or speak on behalf of, and understand means to comprehend. A litigant cannot disable legal proceedings by announcing private alternate meanings for common words."
        ),
        "court_reality": (
            "Judges reject this because legal interpretation is based on accepted usage, statutory context, precedent, and ordinary meaning, not improvised linguistic demolition."
        ),
        "judicial_pushback": (
            "Typical bench response: that is not what those words mean in this courtroom, and your personal redefinition does not alter the proceeding."
        ),
        "semantic_trick": (
            "This whole topic is the semantic trick: taking words apart and pretending syllables outrank dictionaries, context, and centuries of actual use."
        ),
        "parody_citation": "Claimed authority stack: syllable scissors + dictionary fragments + absolute confidence that etymology is a force field."
    },
    {
        "title": "Self-Representation / Lawyer Mockery Reversal",
        "aliases": [
            "represent yourself",
            "brain surgery on yourself",
            "pro se",
            "I do not need a lawyer",
            "attorney trap"
        ],
        "tags": [
            "self representation", "pro se", "lawyer", "brain surgery", "attorney", "judge"
        ],
        "sovcit_claim": (
            "I do not need counsel because attorneys are officers of the court and therefore part of the fraud. I can speak for myself better than any licensed actor in a robe cartel."
        ),
        "sovcit_explanation": (
            "This argument overlaps with general anti-lawyer distrust and the sovereign-citizen belief that ordinary legal procedure is a trick system. It often appears beside contempt for legal training, paired with total confidence in self-created pseudo-law."
        ),
        "flaw_summary": (
            "A person may often choose self-representation, but that does not make self-representation wise, and it certainly does not make pseudo-legal arguments valid."
        ),
        "legal_reality": (
            "Many courts allow self-representation under specific rules, but judges repeatedly warn that the person is still held to procedural and substantive law. The right to represent yourself is not a right to substitute fantasy doctrine for legal argument."
        ),
        "court_reality": (
            "Judges reject the associated nonsense because being pro se does not exempt anyone from legal standards. That is why bench comments often compare it to doing brain surgery on yourself: allowed is not the same as advisable."
        ),
        "judicial_pushback": (
            "Typical bench response: you may represent yourself, but you will be held to the same rules as counsel, and this court strongly advises against amateur pseudo-law."
        ),
        "semantic_trick": (
            "Common trick: conflating the right of self-representation with proof that professional legal knowledge is unnecessary or fraudulent."
        ),
        "parody_citation": "Claimed authority stack: anti-lawyer rage + YouTube university + complete faith that confidence beats procedure."
    }
]


class SovCitApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(APP_GEOMETRY)
        self.root.minsize(1180, 720)

        self.topics = TOPICS
        self.title_index = {topic["title"]: topic for topic in self.topics}
        self.mode_var = tk.StringVar(value="Balanced")
        self.search_var = tk.StringVar()
        self.topic_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready.")

        self._build_style()
        self._build_ui()
        self._populate_dropdown()
        self.display_topic(self.topics[0], source_label="Loaded default topic")

    def _build_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 9))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Minor.TButton", font=("Segoe UI", 9), padding=6)

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=10)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 8))

        ttk.Label(header, text=APP_TITLE, style="Header.TLabel").pack(side="left")
        ttk.Label(
            header,
            text="Parody on the left. Reality on the right.",
            style="Status.TLabel"
        ).pack(side="left", padx=(14, 0), pady=(6, 0))

        controls = ttk.LabelFrame(outer, text="Controls", padding=10)
        controls.pack(fill="x", pady=(0, 8))

        row1 = ttk.Frame(controls)
        row1.pack(fill="x")

        ttk.Label(row1, text="Search:").pack(side="left")
        search_entry = ttk.Entry(row1, textvariable=self.search_var, width=42)
        search_entry.pack(side="left", padx=(6, 8))
        search_entry.bind("<Return>", lambda event: self.search_topics())

        ttk.Button(row1, text="Search", style="Action.TButton", command=self.search_topics).pack(side="left", padx=(0, 6))
        ttk.Button(row1, text="Random Claim", style="Action.TButton", command=self.random_topic).pack(side="left", padx=(0, 6))
        ttk.Button(row1, text="Clear", style="Action.TButton", command=self.clear_all).pack(side="left", padx=(0, 6))

        ttk.Label(row1, text="Mode:").pack(side="left", padx=(16, 6))
        mode_box = ttk.Combobox(row1, textvariable=self.mode_var, state="readonly", width=14)
        mode_box["values"] = ["Balanced", "Dry Legal", "Extra Parody"]
        mode_box.pack(side="left")
        mode_box.bind("<<ComboboxSelected>>", lambda event: self.refresh_current_topic())

        row2 = ttk.Frame(controls)
        row2.pack(fill="x", pady=(10, 0))

        ttk.Label(row2, text="Topic:").pack(side="left")
        self.topic_combo = ttk.Combobox(row2, textvariable=self.topic_var, state="readonly", width=46)
        self.topic_combo.pack(side="left", padx=(6, 8))
        self.topic_combo.bind("<<ComboboxSelected>>", lambda event: self.load_selected_topic())

        ttk.Label(row2, text="Closest matches:").pack(side="left", padx=(12, 6))
        self.match_list = tk.Listbox(row2, height=4, width=42, exportselection=False)
        self.match_list.pack(side="left", fill="x", expand=True)
        self.match_list.bind("<<ListboxSelect>>", lambda event: self.load_match_selection())
        self.match_list.bind("<Double-Button-1>", lambda event: self.load_match_selection())

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self.left_text = self._build_panel(body, 0, "SovCit Claim / Framing")
        self.right_text = self._build_panel(body, 1, "Reality Check / Legal Breakdown")

        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(8, 0))

        ttk.Button(bottom, text="Copy Left", style="Minor.TButton", command=lambda: self.copy_text(self.left_text)).pack(side="left", padx=(0, 6))
        ttk.Button(bottom, text="Copy Right", style="Minor.TButton", command=lambda: self.copy_text(self.right_text)).pack(side="left", padx=(0, 6))
        ttk.Button(bottom, text="Copy Both", style="Minor.TButton", command=self.copy_both).pack(side="left", padx=(0, 12))

        ttk.Label(bottom, textvariable=self.status_var, style="Status.TLabel").pack(side="left", pady=(4, 0))

    def _build_panel(self, parent, column, title):
        panel = ttk.LabelFrame(parent, text=title, padding=8)
        panel.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 6, 6 if column == 0 else 0))
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)

        text = tk.Text(panel, wrap="word", font=("Segoe UI", 10), undo=False)
        text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text.configure(yscrollcommand=scrollbar.set)

        text.tag_configure("title", font=("Segoe UI", 14, "bold"))
        text.tag_configure("heading", font=("Segoe UI", 11, "bold"))
        text.tag_configure("body", font=("Segoe UI", 10))
        text.tag_configure("mono", font=("Consolas", 10))
        return text

    def _populate_dropdown(self):
        titles = [topic["title"] for topic in self.topics]
        self.topic_combo["values"] = titles
        if titles:
            self.topic_var.set(titles[0])

    def tokenize(self, text: str):
        words = re.findall(r"[a-zA-Z0-9']+", text.lower())
        return [w for w in words if w not in STOPWORDS and len(w) > 1]

    def normalized_blob(self, topic):
        pieces = [
            topic["title"],
            " ".join(topic.get("aliases", [])),
            " ".join(topic.get("tags", [])),
            topic.get("sovcit_claim", ""),
            topic.get("sovcit_explanation", ""),
            topic.get("flaw_summary", ""),
            topic.get("legal_reality", ""),
        ]
        return " ".join(pieces).lower()

    def score_topic(self, query: str, topic):
        q = query.strip().lower()
        if not q:
            return 0.0

        title = topic["title"].lower()
        aliases = [a.lower() for a in topic.get("aliases", [])]
        tags = [t.lower() for t in topic.get("tags", [])]
        blob = self.normalized_blob(topic)

        score = 0.0

        if q == title:
            score += 200

        if q in title:
            score += 80

        for alias in aliases:
            if q == alias:
                score += 140
            elif q in alias:
                score += 70

        for tag in tags:
            if q == tag:
                score += 95
            elif q in tag or tag in q:
                score += 36

        query_tokens = self.tokenize(q)
        blob_tokens = self.tokenize(blob)
        title_tokens = self.tokenize(title)
        alias_tokens = self.tokenize(" ".join(aliases))
        tag_tokens = self.tokenize(" ".join(tags))
        token_counts = Counter(blob_tokens)

        for token in query_tokens:
            if token in title_tokens:
                score += 42
            if token in alias_tokens:
                score += 28
            if token in tag_tokens:
                score += 34
            if token in token_counts:
                score += min(18, 6 + token_counts[token])

        phrase_ratio = difflib.SequenceMatcher(None, q, title).ratio()
        score += phrase_ratio * 55

        best_alias_ratio = max([difflib.SequenceMatcher(None, q, alias).ratio() for alias in aliases], default=0.0)
        score += best_alias_ratio * 44

        # fuzzy word matching for typos / close intent
        for token in query_tokens:
            candidates = title_tokens + alias_tokens + tag_tokens
            if not candidates:
                continue
            best_word_ratio = max(difflib.SequenceMatcher(None, token, cand).ratio() for cand in candidates)
            score += best_word_ratio * 18

        return score

    def search_topics(self):
        query = self.search_var.get().strip()
        if not query:
            self.status_var.set("Enter a search phrase or use Random Claim.")
            self.populate_match_list([])
            return

        ranked = sorted(
            [(self.score_topic(query, topic), topic) for topic in self.topics],
            key=lambda item: item[0],
            reverse=True
        )

        filtered = [(score, topic) for score, topic in ranked if score > 20]
        if not filtered:
            self.populate_match_list([])
            self.status_var.set(f"No strong match found for '{query}'.")
            return

        top_matches = filtered[:5]
        self.populate_match_list([topic["title"] for _, topic in top_matches])

        best_score, best_topic = top_matches[0]
        self.topic_var.set(best_topic["title"])
        self.display_topic(best_topic, source_label=f"Best match for: {query}")

        if len(top_matches) > 1:
            self.status_var.set(f"Loaded best match for '{query}'. {len(top_matches)} close matches listed.")
        else:
            self.status_var.set(f"Loaded match for '{query}'.")

    def populate_match_list(self, titles):
        self.match_list.delete(0, tk.END)
        for title in titles:
            self.match_list.insert(tk.END, title)

    def load_match_selection(self):
        selection = self.match_list.curselection()
        if not selection:
            return
        title = self.match_list.get(selection[0])
        topic = self.title_index.get(title)
        if topic:
            self.topic_var.set(title)
            self.display_topic(topic, source_label="Loaded from closest matches")
            self.status_var.set(f"Loaded: {title}")

    def load_selected_topic(self):
        title = self.topic_var.get()
        topic = self.title_index.get(title)
        if topic:
            self.display_topic(topic, source_label="Loaded from dropdown")
            self.status_var.set(f"Loaded: {title}")

    def random_topic(self):
        topic = random.choice(self.topics)
        self.topic_var.set(topic["title"])
        self.display_topic(topic, source_label="Random topic")
        self.status_var.set(f"Randomized: {topic['title']}")

    def clear_all(self):
        self.search_var.set("")
        self.match_list.delete(0, tk.END)
        self.left_text.delete("1.0", tk.END)
        self.right_text.delete("1.0", tk.END)
        self.status_var.set("Cleared.")

    def refresh_current_topic(self):
        title = self.topic_var.get().strip()
        topic = self.title_index.get(title)
        if topic:
            self.display_topic(topic, source_label="Mode updated")
            self.status_var.set(f"Mode set to {self.mode_var.get()}.")

    def display_topic(self, topic, source_label=""):
        self.left_text.delete("1.0", tk.END)
        self.right_text.delete("1.0", tk.END)

        mode = self.mode_var.get()

        left_sections = self.build_left_content(topic, mode)
        right_sections = self.build_right_content(topic, mode)

        self.render_sections(self.left_text, left_sections)
        self.render_sections(self.right_text, right_sections)

        if source_label:
            self.status_var.set(f"{source_label}: {topic['title']}")

    def build_left_content(self, topic, mode):
        intro = {
            "Balanced": "Presented in typical sovereign-citizen framing.",
            "Dry Legal": "Presented as the core pseudo-legal claim without extra performance fluff.",
            "Extra Parody": "Presented in extra-theatrical sovereign-citizen style for comedy purposes."
        }[mode]

        claim = topic["sovcit_claim"]
        explanation = topic["sovcit_explanation"]
        citation = topic.get("parody_citation", "")

        if mode == "Dry Legal":
            citation = ""
        elif mode == "Extra Parody":
            claim = self.parody_up(claim)
            explanation = self.parody_up(explanation)

        return [
            ("title", topic["title"]),
            ("heading", "Overview"),
            ("body", intro),
            ("heading", "Claim"),
            ("body", claim),
            ("heading", "How They Usually Frame It"),
            ("body", explanation),
            ("heading", "Mock Citation Stack"),
            ("body", citation if citation else "Suppressed in Dry Legal mode."),
        ]

    def build_right_content(self, topic, mode):
        flaw = topic["flaw_summary"]
        reality = topic["legal_reality"]
        court = topic["court_reality"]

        if mode == "Extra Parody":
            flaw += " In other words: saying it louder does not upgrade it into law."
            court += " The robe does not become a captain's coat just because someone says 'admiralty' in a landlocked courtroom."
        elif mode == "Dry Legal":
            court = topic["court_reality"]

        return [
            ("title", topic["title"]),
            ("heading", "Main Flaw"),
            ("body", flaw),
            ("heading", "Actual Legal Reality"),
            ("body", reality),
            ("heading", "Why Courts Reject It"),
            ("body", court),
        ]

    def parody_up(self, text: str):
        replacements = {
            "court": "tribunal of suspicious carpeted authority",
            "law": "mystical paperwork regime",
            "license": "state permission talisman",
            "vehicle": "rolling declaration of personal freedom",
            "driver": "alleged operator",
            "person": "so-called statutory being",
            "jurisdiction": "magic robe radius",
        }
        out = text
        for old, new in replacements.items():
            out = re.sub(rf"\b{re.escape(old)}\b", new, out, flags=re.IGNORECASE)
        return out

    def render_sections(self, widget, sections):
        for style_name, content in sections:
            if not content:
                continue
            widget.insert(tk.END, content + "\n\n", style_name)
        widget.see("1.0")

    def copy_text(self, widget):
        content = widget.get("1.0", tk.END).strip()
        if not content:
            self.status_var.set("Nothing to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()
        self.status_var.set("Copied to clipboard.")

    def copy_both(self):
        left = self.left_text.get("1.0", tk.END).strip()
        right = self.right_text.get("1.0", tk.END).strip()
        if not left and not right:
            self.status_var.set("Nothing to copy.")
            return

        combined = (
            "=== LEFT PANEL: SOVCIT CLAIM / FRAMING ===\n\n" + left +
            "\n\n=== RIGHT PANEL: REALITY CHECK / LEGAL BREAKDOWN ===\n\n" + right
        )
        self.root.clipboard_clear()
        self.root.clipboard_append(combined)
        self.root.update()
        self.status_var.set("Copied both panels to clipboard.")


def main():
    root = tk.Tk()
    app = SovCitApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
