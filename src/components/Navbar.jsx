import React, { useState, useEffect } from 'react';
import { Terminal, Download, Menu, X, ExternalLink, ChevronRight } from 'lucide-react';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'À propos', href: '#about' },
    { name: 'Compétences', href: '#skills' },
    { name: 'Réalisations', href: '#projects' },
    { name: 'Certifications', href: '#certifications' },
    { name: 'Console IBM i', href: '#terminal' },
    { name: 'Contact', href: '#contact' },
  ];

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled 
        ? 'bg-[#030712]/90 backdrop-blur-md border-b border-slate-800/80 shadow-lg shadow-black/20 py-3' 
        : 'bg-transparent py-5'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo / Brand */}
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-blue-700 via-blue-600 to-cyan-400 p-[1px] shadow-md shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-all">
              <div className="w-full h-full bg-[#070d1e] rounded-[7px] flex items-center justify-center font-mono font-bold text-white text-base">
                YE
              </div>
            </div>
            <div>
              <span className="font-semibold text-slate-100 text-base tracking-tight block group-hover:text-blue-400 transition-colors">
                Yassine EL OUARDI
              </span>
              <span className="text-xs text-blue-400 font-mono block">
                Analyste Développeur IBM i
              </span>
            </div>
          </a>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-900/60 border border-slate-800/70 rounded-full px-4 py-1.5 backdrop-blur-sm">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="text-xs lg:text-sm font-medium text-slate-300 hover:text-white px-3 py-1.5 rounded-full hover:bg-slate-800/60 transition-all duration-150"
              >
                {link.name}
              </a>
            ))}
          </nav>

          {/* CTA Desktop */}
          <div className="hidden lg:flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              Disponible
            </div>

            <a
              href="/CV_Yassine_EL_Ouardi_Analyste_Developpeur_IBM_i_AS400.pdf"
              download="CV_Yassine_EL_Ouardi_IBM_i.pdf"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs tracking-wide shadow-md shadow-blue-600/30 hover:shadow-blue-600/50 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>CV (PDF)</span>
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center gap-2">
            <a
              href="/CV_Yassine_EL_Ouardi_Analyste_Developpeur_IBM_i_AS400.pdf"
              download="CV_Yassine_EL_Ouardi_IBM_i.pdf"
              className="p-2 rounded-lg bg-blue-600 text-white text-xs"
              title="Télécharger CV"
            >
              <Download className="w-4 h-4" />
            </a>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile menu dropdown */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-3 pt-3 pb-4 border-t border-slate-800 bg-[#070d1e]/95 backdrop-blur-xl rounded-2xl p-4 shadow-xl">
            <div className="flex flex-col gap-2">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center justify-between text-sm font-medium text-slate-200 hover:text-blue-400 py-2 px-3 rounded-lg hover:bg-slate-800/50"
                >
                  <span>{link.name}</span>
                  <ChevronRight className="w-4 h-4 text-slate-500" />
                </a>
              ))}
              <div className="pt-3 mt-2 border-t border-slate-800 flex items-center justify-between">
                <span className="flex items-center gap-2 text-xs font-mono text-emerald-400">
                  <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
                  Casablanca, Maroc
                </span>
                <a
                  href="https://www.linkedin.com/in/yassine-el-ouardi-as400/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-400 flex items-center gap-1 hover:underline"
                >
                  LinkedIn <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
