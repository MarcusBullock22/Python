import React, { useEffect, useState } from "react";
import { motion, useScroll, useSpring } from "framer-motion";
import { ArrowRight, Download, Github, Linkedin, Twitter, Mail, MapPin, Phone, Sparkles, ExternalLink, Briefcase, LibraryBig, Cpu, Trophy, ChevronDown, Star, Code2, Database, Rocket, Shield } from "lucide-react";
import { Toaster, toast } from "sonner";
import emailjs from "@emailjs/browser";
emailjs.init(import.meta.env.VITE_EMAILJS_PUBLIC_KEY); 

const profile = {
  name: "Marcus Bullock",
  title: "Senior Data Engineer",
  tagline: "Building reliable data systems and applied AI for real missions in the DoD space.",
  location: "Fayetteville, NC · USA",
  email: "marcbullock22@gmail.com",
  phone: "+1",
  resumeUrl: "/Marcus_Bullocks_Data_Engineer_Resume.docx",
  socials: {
    github: "https://github.com/MarcusBullock22",
    linkedin: "https://www.linkedin.com/in/marcusbullock12/",
    Twitter: "https://x.com/MarcBullock2022",
  },
  highlights: [
    { icon: <Shield className="w-4 h-4"/>, text: "Currently Employer: Halvik" },
    { icon: <Rocket className="w-4 h-4"/>, text: "Shipped ML & data pipelines end‑to‑end" },
    { icon: <Database className="w-4 h-4"/>, text: "Azure · SQL · Python · Power BI" },
  ],
};

const about = {
  intro:
    "I’m a Senior Data Engineer who loves hard problems, clean data models, and shipping things that matter. I build secure, scalable data products end to end—Azure, Databricks, SQL, Python, and Power BI—then make them usable with great UX.",
  highlights: [
    "DoD contractor experience",
    "Built ETL/ELT + Lakehouse pipelines",
    "Operational analytics & KPI scorecards",
    "Power BI dashboards with DAX/RLS",
    "APIs, CI/CD, RBAC, governance",
    "Full stack development (webapps and winapps)",
  ],
  fun: [
    "RuneScape grinder, project tinkerer",
    "Building a Scholarship AI agent",
    "MTG landfall enjoyer (Omnath)",
    "Avid reader of sci-fi & fantasy",
  ],
};


const posts = [
  {
    title: "What I Learned Shipping a Streamlit Tool",
    date: "2025-11-02",
    tags: ["Python", "Streamlit", "DevOps"],
    excerpt: "From cold starts to auth: small things that make a lightweight app feel production ready.",
    content: `
      **Problem.** Cold starts and flaky auth…
      **Approach.** Cached session, prewarm ping, secrets via env…
      **Result.** 30% faster first render, fewer 401s…`,
    href: "" // leave empty to use modal
  },
  // …
];


const experience = [
  {
    company: "Halvik (Prime) & GDIT (Sub)",
    role: "Senior Data Engineer & Data Scientist",
    period: "Aug 2023 – Present",
    blurb: "Driving mission-critical data engineering and AI efforts across the U.S. Army’s Special Operations Command, delivering secure, scalable pipelines and operational analytics.",
    bullets: [
      "Architected and deployed end-to-end ML pipelines and reporting APIs in Azure Databricks and SQL Server, accelerating decision cycles for analysts and command teams.",
      "Built governed self-service analytics with Power BI and Collibra, improving data quality, usability, and lineage across classified and unclassified environments.",
      "Productionized LLM-powered workflows for document triage and intelligence brief generation in ADE (All-Domain Environment), reducing manual effort by 60%+.",
      "Automated integration between Vantage, SharePoint, and internal SQL data sources, enabling seamless ingestion for mission dashboards.",
      "Partnered with military and civilian stakeholders to gather requirements, ship enhancements, and reduce time-to-insight with reusable data contracts and APIs.",
    ],
    tags: [
      "Azure",
      "Databricks",
      "Python",
      "SQL",
      "LLMs",
      "Power BI",
      "Collibra",
      "APIs",
      "DevOps",
    ],
  },
  {
    company: "AgAmerica Lending",
    role: "Data Engineer",
    period: "Mar 2023 – Aug 2023",
    blurb: "Modernized data infrastructure and automated cloud workflows to support financial analytics and lending operations.",
    bullets: [
      "Built and automated Azure Data Factory ELT pipelines to unify Salesforce, Yardi, and third-party sources into governed analytics models.",
      "Implemented CI/CD pipelines across Development, QA, and Production environments using Azure DevOps, enabling safe and repeatable ADF deployments.",
      "Optimized database structures and rewritten SQL stored procedures, reducing report latency by 35% and improving operational SLA compliance.",
      "Developed Power BI dashboards and financial models that increased visibility into land value analytics and borrower risk scoring.",
    ],
    tags: ["Azure", "ADF", "Azure DevOps", "SQL", "CI/CD", "Power BI", "Python"],
  },
  {
    company: "Data Age Business Systems",
    role: "Software Engineer → Mid-Level Developer",
    period: "Nov 2017 – Feb 2024",
    blurb: "Led modernization of .NET systems, SSRS reporting, and real-time data tools for 600+ retail and financial customers.",
    bullets: [
      "Built internal .NET Core messaging services and barcode scanning tools integrated with Azure Service Bus.",
      "Owned SQL Server report development, debugging, and customer-facing data workflows for transactional systems.",
      "Refactored legacy FoxPro functionality while engineering high-value enhancements in C#/.NET and SSRS.",
    ],
    tags: [".NET", "SQL Server", "SSRS", "Azure", "C#", "Legacy Support"],
  },
  {
    company: "Kingston Healthcare",
    role: "Help Desk Specialist",
    period: "Apr 2016 – Oct 2017",
    blurb: "Delivered enterprise-level IT support and automation for a multi-location healthcare provider network.",
    bullets: [
      "Automated Active Directory account provisioning using PowerShell, reducing onboarding time by 50% across 30+ facilities.",
      "Provided Tier 2 support for SCCM, Cisco networking, and Windows Server-based systems across the enterprise.",
      "Implemented identity and access controls with Group Policy Objects (GPOs), improving audit compliance and role accuracy.",
    ],
    tags: ["PowerShell", "Active Directory", "Windows Server", "SCCM", "Networking"],
  },
];

function ProjectFilters({ value, onChange, groups }) {
  return (
    <div className="flex flex-wrap gap-2">
      {groups.map((g) => {
        const active = g === value;
        return (
          <button
            key={g}
            type="button"
            onClick={() => onChange(g)}
            className={`px-3 py-1.5 rounded-full text-sm border transition
              ${active
                ? "bg-black text-white border-black dark:bg-white dark:text-black dark:border-white"
                : "bg-white/60 dark:bg-white/5 border-slate-200 dark:border-slate-800 hover:bg-white/80 dark:hover:bg-white/10"
              }`}
          >
            {g}
          </button>
        );
      })}
    </div>
  );
}

const projects = [
  {
    name: "All Along the Jordans",
    group: "Games", 
    desc: "A 64 bit turnbased game built with adobe flash, featuring a unique story and funny animations. Project is currently being reworked in C# due to flash no longer being supported.",
    links: [
      { label: "Play Now (not yet available)", href: "", icon: <ExternalLink className="w-4 h-4" /> },
      { label: "Repo", href: "https://github.com/MarcusBullock22/Game-Creations/tree/master/Final_game", icon: <Code2 className="w-4 h-4" /> },
    ],
    stack: ["Flash", "C#"],
  },
  {
    name: "RuneScape Item Mercher",
    group: "AI",
    desc: "Automates price checks and flipping strategies; passive in-game income with risk controls.",
    links: [
      { label: "Live Demo", href: "https://marcusbullock22-python-runescapeitemmerchermain-usrsts.streamlit.app/", icon: <ExternalLink className="w-4 h-4" /> },
      { label: "Repo", href: "https://github.com/MarcusBullock22/Python/tree/main/RunescapeItemMercher", icon: <Code2 className="w-4 h-4" /> },
    ],
    stack: ["Python", "Pandas", "Streamlit", "Requests"],
  },
  {
  name: "Scholarship Updater (AI Automation)",
  group: "AI",
  desc: "Automated scholarship discovery and tracking system that scrapes eligibility data, updates active opportunities, and uses an AI personality layer to generate tailored scholarship essays.",
  links: [
    { label: "Repo", href: "https://github.com/MarcusBullock22/Python/tree/main/ScholarshipApp", icon: <ExternalLink className="w-4 h-4" /> },
  ],
  stack: ["Python", "Web Scraping", "GPT-4", "Streamlit", "APIs"],
 },
];


const skills = {
  core: [
    "Python", "SQL / T‑SQL", "Databricks", "Azure Data Factory", "Power BI", "APIs", "Data Modeling", "MLOps",
  ],
  ai: ["LLMs", "Prompt Engineering", "Vector Search", "Document AI"],
  de: ["Pipelines", "Orchestration", "Data Contracts", "Testing"],
  soft: ["Stakeholder Comms", "Roadmapping", "Mentorship"],
};

const certs = [
  { title: "Master of Science – Data Analytics", org: "SNHU (2026)" },
  { title: "Bachelor of Science – Computer Science", org: "SNHU (2021)" },
  { title: "Microsoft Power BI – Use Power BI Desktop to Create Reports and Dashboards", org: "The National Registry of CPE Sponsors" },
  { title: "Create Mapping Data Flows in Azure Data Factory", org: "Coursera" },
];


const goTo = (id) => {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
};

const Nav = ({ items, active, onClick }) => {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 120, damping: 20, mass: 0.2 });
  return (
    <div className="fixed top-0 inset-x-0 z-50 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:supports-[backdrop-filter]:bg-slate-900/60 border-b border-white/10 dark:border-slate-800/50">
      <motion.div style={{ scaleX }} className="bg-gradient-to-r from-blue-600 to-cyan-500" />
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex items-center justify-between h-14">
        <button onClick={() => goTo("hero")} className="group flex items-center gap-2 font-semibold">
          <Sparkles className="w-5 h-5 group-hover:rotate-12 transition" />
          <span>Marcus</span>
        </button>
        <ul className="hidden md:flex items-center gap-1">
          {items.map((it) => (
            <li key={it.id}>
              <button
                onClick={() => onClick(it.id)}
                className={`px-3 py-2 rounded-xl text-sm transition font-medium hover:bg-black/5 dark:hover:bg-white/5 ${active === it.id ? "text-blue-600 dark:text-blue-400" : "text-slate-700 dark:text-slate-200"}`}
              >
                {it.label}
              </button>
            </li>
          ))}
        </ul>
        <div className="flex items-center gap-2">
          <a href={profile.socials.github} target="_blank" rel="noreferrer" className="p-2 rounded-lg hover:bg-black/5 dark:hover:bg-white/5" aria-label="GitHub">
            <Github className="w-5 h-5" />
          </a>
          <a href={profile.socials.linkedin} target="_blank" rel="noreferrer" className="p-2 rounded-lg hover:bg-black/5 dark:hover:bg-white/5" aria-label="LinkedIn">
            <Linkedin className="w-5 h-5" />
          </a>
          <a href={profile.socials.Twitter} target="_blank" rel="noreferrer" className="p-2 rounded-lg hover:bg-black/5 dark:hover:bg-white/5" aria-label="X">
            <Twitter className="w-5 h-5" />
          </a>
          <a href={`mailto:${profile.email}`} className="hidden sm:inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white text-sm font-semibold shadow-sm hover:shadow transition">
            <Mail className="w-4 h-4" /> Contact
          </a>
        </div>
      </nav>
    </div>
  );
};

const Hero = () => (
  <section id="hero" className="relative min-h-[92vh] flex items-center overflow-hidden">
    <div aria-hidden className="pointer-events-none absolute inset-0">
      <div className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full bg-blue-500/20 blur-3xl "/>
      <div className="absolute -bottom-40 -right-40 w-[600px] h-[600px] rounded-full bg-blue-500/20 blur-3xl"/>
    </div>

    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 grid lg:grid-cols-2 gap-10 items-center">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
        <div className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/60 dark:bg-white/5 backdrop-blur px-3 py-1 text-xs font-medium">
          <Star className="w-3.5 h-3.5 text-amber-500"/> Open to impactful problems
        </div>
        <h1 className="mt-6 text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight">
          {profile.title}
        </h1>
        <p className="mt-4 text-slate-700 dark:text-slate-300 text-lg leading-relaxed">
          {profile.tagline}
        </p>
        <ul className="mt-6 flex flex-wrap gap-3">
          {profile.highlights.map((h, i) => (
            <li key={i} className="flex items-center gap-2 text-sm px-3 py-2 rounded-xl bg-white/60 dark:bg-white/5 border border-white/20">
              {h.icon}
              <span>{h.text}</span>
            </li>
          ))}
        </ul>
        <div className="mt-8 flex flex-wrap gap-3">
          <a
            href={profile.resumeUrl}
            download
            className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold shadow-lg hover:shadow-xl transition"
          >
            <Download className="w-4 h-4"/> Download Resume
          </a>
          <a
            href="#projects"
            onClick={(e) => { e.preventDefault(); goTo("projects"); }}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5 font-semibold hover:bg-white/80 dark:hover:bg-white/10"
          >
            View Projects <ArrowRight className="w-4 h-4"/>
          </a>
        </div>
        <div className="mt-8 flex items-center gap-4 text-sm text-slate-600 dark:text-slate-400">
          <MapPin className="w-4 h-4"/> {profile.location}
          <Phone className="w-4 h-4"/> {profile.phone}
        </div>
      </motion.div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1, duration: 0.6 }} className="relative">
        <div className="relative rounded-3xl p-1 bg-gradient-to-br from-white/40 to-white/10 dark:from-white/10 dark:to-white/5 backdrop-blur border border-white/20 shadow-2xl">
          <div className="rounded-3xl p-8 bg-white/70 dark:bg-slate-900/60">
            <div className="flex items-center gap-3 text-xs font-medium text-slate-500 dark:text-slate-400">
              <div className="w-2 h-2 rounded-full bg-emerald-400"/> On Mission
            </div>
            <div className="mt-4 grid grid-cols-3 sm:grid-cols-4 gap-3">
              {[
                { icon: <Cpu className="w-5 h-5"/>, label: "Python" },
                { icon: <Database className="w-5 h-5"/>, label: "SQL" },
                { icon: <LibraryBig className="w-5 h-5"/>, label: "Power BI" },
                { icon: <Code2 className="w-5 h-5"/>, label: "APIs" },
                { icon: <Rocket className="w-5 h-5"/>, label: "Azure" },
                { icon: <Briefcase className="w-5 h-5"/>, label: "Databricks" },
                { icon: <Sparkles className="w-5 h-5"/>, label: "LLMs" },
                { icon: <Shield className="w-5 h-5"/>, label: "Governance" },
              ].map((s, i) => (
                <div key={i} className="rounded-2xl p-4 bg-gradient-to-r from-blue-600 to-cyan-500 dark:from-blue-950/40 dark:to-cyan-950/40 border border-white/20 text-center">
                  <div className="mx-auto w-10 h-10 flex items-center justify-center rounded-xl bg-white/70 dark:bg-white/10 mb-2">
                    {s.icon}
                  </div>
                  <div className="text-sm font-semibold">{s.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="absolute -bottom-8 left-0 right-0 flex justify-center">
          <button onClick={() => goTo("experience")} className="group inline-flex items-center gap-2 text-sm px-4 py-2 rounded-full bg-black/80 text-white shadow-lg">
            Scroll for more <ChevronDown className="w-4 h-4 group-hover:translate-y-0.5 transition"/>
          </button>
        </div>
      </motion.div>
    </div>
  </section>
);

const Section = ({ id, label, children }) => (
  <section id={id} className="scroll-mt-24 py-20">
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight flex items-center gap-2">
        <span className="inline-flex w-1.5 h-6 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-full"/>
        {label}
      </h2>
      <div className="mt-8">{children}</div>
    </div>
  </section>
);

const About = () => (
  <Section id="about" label="About Me">
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Intro card */}
      <div className="lg:col-span-2 rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
        <h3 className="text-lg font-bold">Hi, I’m Marcus</h3>
        <p className="mt-2 text-slate-700 dark:text-slate-300">{about.intro}</p>

        <div className="mt-4">
          <h4 className="text-sm font-semibold uppercase text-slate-600 dark:text-slate-400">What I’m good at</h4>
          <ul className="mt-2 grid sm:grid-cols-2 gap-2 text-sm">
            {about.highlights.map((x, i) => (
              <li key={i} className="flex items-center gap-2">
                <span className="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500" /> {x}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Fun/personal card */}
      <div className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
        <h4 className="text-sm font-semibold uppercase text-slate-600 dark:text-slate-400">Outside of work</h4>
        <ul className="mt-3 space-y-2 text-sm">
          {about.fun.map((x, i) => (
            <li key={i} className="flex items-center gap-2">
              <span className="inline-block w-1.5 h-1.5 rounded-full bg-cyan-500" /> {x}
            </li>
          ))}
        </ul>
      </div>
    </div>
  </Section>
);

function PostCard({ p }) {
  return (
    <article className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-lg font-semibold">{p.title}</h3>
        <span className="text-xs px-2 py-1 rounded-full bg-white/60 dark:bg-white/10 border border-slate-200 dark:border-slate-800">
          {new Date(p.date).toLocaleDateString()}
        </span>
      </div>
      <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">{p.excerpt}</p>
      {p.tags?.length ? (
        <div className="mt-3 flex flex-wrap gap-2">
          {p.tags.map((t, i) => (
            <span key={i} className="text-xs px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
              {t}
            </span>
          ))}
        </div>
      ) : null}
      <div className="mt-4">
        <a
          href={p.href || "#"}
          className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5 hover:bg-white/80 dark:hover:bg-white/10"
        >
          Read more
          <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    </article>
  );
}

function NoteCard({ p, onOpen }) {
  return (
    <article className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-lg font-semibold">{p.title}</h3>
        <span className="text-xs px-2 py-1 rounded-full bg-white/60 dark:bg-white/10 border border-slate-200 dark:border-slate-800">
          {new Date(p.date).toLocaleDateString()}
        </span>
      </div>
      <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">{p.excerpt}</p>
      {p.tags?.length ? (
        <div className="mt-3 flex flex-wrap gap-2">
          {p.tags.map((t, i) => (
            <span key={i} className="text-xs px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
              {t}
            </span>
          ))}
        </div>
      ) : null}

      <div className="mt-4">
        {p.href
          ? (
            <a
              href={p.href}
              className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5 hover:bg-white/80 dark:hover:bg-white/10"
              target="_blank" rel="noopener noreferrer"
            >
              Read more <ArrowRight className="w-4 h-4" />
            </a>
          )
          : (
            <button
              onClick={() => onOpen(p)}
              className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5 hover:bg-white/80 dark:hover:bg-white/10"
            >
              Read more <ArrowRight className="w-4 h-4" />
            </button>
          )}
      </div>
    </article>
  );
}


const Notes = () => {
  const [open, setOpen] = React.useState(false);
  const [current, setCurrent] = React.useState(null);

  const onOpen = (p) => { setCurrent(p); setOpen(true); };
  const onClose = () => setOpen(false);

  return (
    <Section id="notes" label="Notes & Blog">
      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
        {posts.map((p, i) => <NoteCard key={i} p={p} onOpen={onOpen} />)}
      </div>
      {/* Modal */}
      {open && current && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/60" onClick={onClose} />
          <div className="absolute inset-0 grid place-items-center p-4">
            <div className="w-full max-w-2xl rounded-2xl p-6 border border-white/20 bg-white/90 dark:bg-slate-900/90 backdrop-blur">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-xl font-bold">{current.title}</h3>
                  <div className="mt-1 text-xs text-slate-600 dark:text-slate-400">
                    {new Date(current.date).toLocaleDateString()}
                  </div>
                </div>
                <button onClick={onClose} className="px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-800">
                  Close
                </button>
              </div>

              <div className="prose dark:prose-invert mt-4 max-w-none">
                {/* If you want Markdown support later, we can add it; for now, simple line breaks */}
                {current.content
                  ? current.content.split("\n").map((line, i) => <p key={i}>{line}</p>)
                  : <p>No additional content yet.</p>}
              </div>
            </div>
          </div>
        </div>
      )}
    </Section>
  );
};


const Experience = () => (
  <Section id="experience" label="Experience">
    <div className="grid md:grid-cols-2 gap-6">
      {experience.map((job, idx) => (
        <motion.article
          key={idx}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.5 }}
          className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur"
        >
          <div className="flex items-center justify-between gap-3">
            <div>
              <h3 className="text-lg font-bold">{job.role}</h3>
              <p className="text-slate-600 dark:text-slate-400">{job.company} · <span className="font-medium">{job.period}</span></p>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full bg-blue-600/10 text-blue-600 dark:text-blue-400 border border-blue-600/20">
              <Briefcase className="w-3.5 h-3.5"/> Role
            </span>
          </div>
          <p className="mt-3 text-sm text-slate-700 dark:text-slate-300">{job.blurb}</p>
          <ul className="mt-4 space-y-2 text-sm">
            {job.bullets.map((b, i) => (
              <li key={i} className="flex gap-2"><span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-emerald-500"/>{b}</li>
            ))}
          </ul>
          <div className="mt-4 flex flex-wrap gap-2">
            {job.tags.map((t) => (
              <span key={t} className="text-xs font-medium px-2 py-1 rounded-md bg-slate-100 dark:bg-slate-800">{t}</span>
            ))}
          </div>
        </motion.article>
      ))}
    </div>
  </Section>
);

const Projects = () => {
  const [filter, setFilter] = React.useState("All");

  // Build group list dynamically from your data
  const groups = React.useMemo(() => {
    const set = new Set(projects.map(p => p.group || "Other"));
    return ["All", ...Array.from(set)];
  }, []);

  const filtered = React.useMemo(() => {
    if (filter === "All") return projects;
    return projects.filter(p => (p.group || "Other") === filter);
  }, [filter]);

  return (
    <Section id="projects" label="Projects">
      <div className="flex items-center justify-between gap-3 mb-6">
        <ProjectFilters value={filter} onChange={setFilter} groups={groups} />
        {/* Optional count */}
        <span className="text-sm text-slate-600 dark:text-slate-400">
          {filtered.length} / {projects.length}
        </span>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
        {filtered.map((p, i) => (
          <div key={i} className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
            <div className="flex items-start justify-between gap-4">
              <h3 className="text-lg font-semibold">{p.name}</h3>
              <span className="text-xs px-2 py-1 rounded-full border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5">
                {p.group || "Other"}
              </span>
            </div>

            <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">{p.desc}</p>

            {p.stack?.length ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {p.stack.map((t, j) => (
                  <span key={j} className="text-xs px-2 py-1 rounded-full bg-slate-100 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
                    {t}
                  </span>
                ))}
              </div>
            ) : null}

            {p.links?.length ? (
              <div className="mt-4 flex flex-wrap gap-2">
                {p.links.map((l, k) => (
                  <a key={k} href={l.href} className="inline-flex items-center gap-2 text-sm px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/60 dark:bg-white/5 hover:bg-white/80 dark:hover:bg-white/10">
                    {l.icon} {l.label}
                  </a>
                ))}
              </div>
            ) : null}
          </div>
        ))}
      </div>
    </Section>
  );
};


const Skills = () => (
  <Section id="skills" label="Skills">
    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
      {Object.entries(skills).map(([k, arr]) => (
        <div key={k} className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
          <div className="text-sm font-semibold uppercase tracking-wider text-slate-500">{k}</div>
          <ul className="mt-3 flex flex-wrap gap-2">
            {arr.map((s) => (
              <li key={s} className="text-xs font-medium px-2 py-1 rounded-md bg-slate-100 dark:bg-slate-800">{s}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  </Section>
);

const Certs = () => (
  <Section id="certs" label="Education & Certifications">
    <div className="grid md:grid-cols-2 gap-6">
      {certs.map((c, i) => (
        <div key={i} className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
          <div className="flex items-center gap-3">
            <Trophy className="w-5 h-5 text-amber-500"/>
            <div>
              <div className="font-semibold">{c.title}</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">{c.org}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  </Section>
);


const Contact = () => {
const sendEmail = async (e) => {
  e.preventDefault();

  const form = e.target;
  const params = {
    from_name: form.from_name.value,
    reply_to: form.reply_to.value,
    message: form.message.value,
  };

  // optional: simple length check before sending
  if (params.message.trim().length < 10) {
    toast.warning("Message is a bit short — add a few more details?");
    return;
  }

  try {
    await toast.promise(
      emailjs.send(
      import.meta.env.VITE_EMAILJS_SERVICE_ID,// Service ID
      import.meta.env.VITE_EMAILJS_TEMPLATE_ID,// Template ID
        params                // Using emailjs.init({ publicKey }) elsewhere
      ),
      {
        loading: "Sending…",
        success: "Message sent! I’ll get back to you soon.",
        error: (err) =>
          err?.text || err?.message || "Send failed. Please try again.",
      }
    );
    form.reset();
  } catch {
    /* toast.promise already showed the error */
  }
};


  return (
    <Section id="contact" label="Contact">
      <div className="grid lg:grid-cols-2 gap-8 items-start">

        {/* Left Panel */}
        <div className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur">
          <h3 className="text-lg font-bold">Let’s build something</h3>
          <p className="mt-2 text-sm text-slate-700 dark:text-slate-300">
            I love hard problems, clean data models, and shipping things that matter. The fastest way to reach me is email.
          </p>
          <div className="mt-4 space-y-2 text-sm">
            <a
              href={`mailto:${profile.email}`}
              className="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-black text-white hover:opacity-90"
            >
              <Mail className="w-4 h-4" /> {profile.email}
            </a>
            <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <Phone className="w-4 h-4" /> {profile.phone}
            </div>
            <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <MapPin className="w-4 h-4" /> {profile.location}
            </div>
          </div>
        </div>

        {/* Form */}
        <form
          onSubmit={sendEmail}
          className="rounded-2xl p-6 border border-white/20 bg-white/70 dark:bg-white/5 backdrop-blur"
        >
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Name</label>
              <input
                name="from_name"
                className="mt-1 w-full px-3 py-2 rounded-xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Your name"
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium">Email</label>
              <input
                type="email"
                name="reply_to"
                className="mt-1 w-full px-3 py-2 rounded-xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="you@company.com"
                required
              />
            </div>
          </div>

          <div className="mt-4">
            <label className="text-sm font-medium">Message</label>
            <textarea
              name="message"
              rows={5}
              className="mt-1 w-full px-3 py-2 rounded-xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Tell me about your project..."
              required
            />
          </div>

          <button
            type="submit"
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl  bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold hover:shadow-lg transition"
          >
            Send Message <ArrowRight className="w-4 h-4" />
          </button>
        </form>

      </div>
    </Section>
  );
};


function useActiveSection(ids) {
  const [active, setActive] = useState(ids[0]);
  useEffect(() => {
    const obs = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            setActive(e.target.id);
            break;
          }
        }
      },
      { rootMargin: "-40% 0px -59% 0px", threshold: [0, 0.25, 0.6, 1] }
    );
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) obs.observe(el);
    });
    return () => obs.disconnect();
  }, [ids.join(",")]);
  return [active, setActive];
}

function NavWrapper({ sections, active, onClick }) {
  return <Nav items={sections} active={active} onClick={onClick} />;
}

export default function PortfolioSite() {
  const sections = [
    { id: "hero", label: "Home" },
    { id: "experience", label: "Experience" },
    { id: "projects", label: "Projects" },
    { id: "skills", label: "Skills" },
    { id: "certs", label: "Education & Certifications" },
    { id: "about", label: "About" },
    { id: "notes", label: "Notes" },
    { id: "contact", label: "Contact" },
  ];

  const [active, setActive] = useActiveSection(sections.map((s) => s.id));

 return (
  <main className="min-h-screen bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">
     <Toaster position="top-right" richColors closeButton />
      <NavWrapper sections={sections} active={active} onClick={(id) => goTo(id)} />
      <Hero />
      <Experience />
      <Projects />
      <Skills />
      <Certs />
      <About />
      <Notes />
      <Contact />
      <footer className="py-10 text-center text-sm text-slate-600 dark:text-slate-400">
        © {new Date().getFullYear()} {profile.name}. All rights reserved.
      </footer>
    </main>
  );
}
