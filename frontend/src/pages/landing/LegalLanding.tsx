/**
 * Legal Services Landing Page
 * Mindframe AI for Law Firms & Legal Departments
 */
import React from 'react';

export const LegalLanding: React.FC = () => {
  return (
    <div className="legal-landing">
      {/* Hero */}
      <section className="hero bg-gradient-to-r from-slate-700 to-slate-900 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-sm font-semibold mb-4">⚖️ LEGAL SOLUTION</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              AI-Drevet Juridisk Analyse som Sparer Timer Hver Dag
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              Automatiser dokumentgjennomgang, kontraktanalyse og compliance-sjekk.
              Reduser billable hours spent på rutinearbeid med 70%.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-slate-700 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
                Start Gratis Prøveperiode
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-slate-700">
                Se Demo
              </button>
            </div>
            <p className="mt-4 text-sm opacity-75">✅ GDPR Compliant • ✅ Encrypted • ✅ Attorney-Client Privilege Protected</p>
          </div>
        </div>
      </section>

      {/* Problem/Solution */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Utfordringer i Juridisk Sektor
          </h2>
          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-red-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-red-600">Problemene</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Tidkrevende dokumentgjennomgang:</strong> 40% av tiden går til lesing</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Dyre junioradvokater:</strong> €50-100/time for rutinearbeid</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Menneskelige feil:</strong> 5-10% risiko for å overse viktige klausuler</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Compliance kompleksitet:</strong> Vanskelig å holde oversikt</div>
                </li>
              </ul>
            </div>

            <div className="bg-green-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-green-600">Mindframe Løsning</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>AI dokumentanalyse:</strong> Gjennomgå 100-siders kontrakter på minutter</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Kostnadsbesparelse:</strong> Erstatt junior-timer med AI (€10 vs €50/t)</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>100% nøyaktighet:</strong> AI fanger ALLE risikoklausuler</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Auto-compliance:</strong> Alltid oppdatert med nyeste regler</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Legal Agents */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            10 Spesialiserte Juridiske AI-Agenter
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📄</div>
              <h3 className="text-xl font-bold mb-2">Contract Analysis AI</h3>
              <p className="text-gray-600 mb-4">
                Analyserer kontrakter. Identifiserer risiko, mangler, uklare klausuler.
              </p>
              <div className="text-sm text-green-600 font-semibold">90% raskere review</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🔍</div>
              <h3 className="text-xl font-bold mb-2">Legal Research Assistant</h3>
              <p className="text-gray-600 mb-4">
                Søker i lovdata, dommer, forskrifter. Finner relevante presedenser.
              </p>
              <div className="text-sm text-green-600 font-semibold">10x raskere research</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">✏️</div>
              <h3 className="text-xl font-bold mb-2">Document Drafting AI</h3>
              <p className="text-gray-600 mb-4">
                Genererer utkast til kontrakter, avtaler, brev basert på templates.
              </p>
              <div className="text-sm text-green-600 font-semibold">70% mindre tid</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">⚠️</div>
              <h3 className="text-xl font-bold mb-2">Compliance Checker</h3>
              <p className="text-gray-600 mb-4">
                Sjekker dokumenter mot GDPR, AML, selskapslov, arbeidsrett.
              </p>
              <div className="text-sm text-green-600 font-semibold">Zero compliance brudd</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📅</div>
              <h3 className="text-xl font-bold mb-2">Deadline Tracker</h3>
              <p className="text-gray-600 mb-4">
                Sporer alle frister. Varsler advokat i god tid før deadline.
              </p>
              <div className="text-sm text-green-600 font-semibold">Zero tapte frister</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💼</div>
              <h3 className="text-xl font-bold mb-2">Case Management System</h3>
              <p className="text-gray-600 mb-4">
                Organiserer alle saker. Dokumenter, notater, tidslinje, kontakter.
              </p>
              <div className="text-sm text-green-600 font-semibold">Alt på ett sted</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💬</div>
              <h3 className="text-xl font-bold mb-2">Client Communication Bot</h3>
              <p className="text-gray-600 mb-4">
                Besvarer rutinespørsmål fra klienter 24/7. Frigjør advokatene.
              </p>
              <div className="text-sm text-green-600 font-semibold">80% auto-resolved</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">⏱️</div>
              <h3 className="text-xl font-bold mb-2">Billable Hours Tracker</h3>
              <p className="text-gray-600 mb-4">
                Automatisk tidsregistrering. Genererer fakturaer til klienter.
              </p>
              <div className="text-sm text-green-600 font-semibold">15% mer fakturert tid</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🔐</div>
              <h3 className="text-xl font-bold mb-2">Secure Document Vault</h3>
              <p className="text-gray-600 mb-4">
                Kryptert lagring av sensitive dokumenter. Full audit trail.
              </p>
              <div className="text-sm text-green-600 font-semibold">Bank-level security</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Legal Analytics Dashboard</h3>
              <p className="text-gray-600 mb-4">
                Analyser win-rate, tidsbruk, lønnsomhet per sakstype.
              </p>
              <div className="text-sm text-green-600 font-semibold">Data-drevet strategi</div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto bg-slate-50 p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-6 text-center">ROI-Kalkulator</h2>
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Junior-timer erstattet (20t/uke × €60)</span>
                  <span className="text-2xl font-bold text-green-600">€62,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Økt billable hours (10% mer)</span>
                  <span className="text-2xl font-bold text-green-600">€80,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Unngåtte compliance-bøter</span>
                  <span className="text-2xl font-bold text-green-600">€50,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Raskere case closure (15%)</span>
                  <span className="text-2xl font-bold text-green-600">€40,000/år</span>
                </div>
              </div>
              <div className="border-t-2 pt-6">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold">Total Årlig Verdi:</span>
                  <span className="text-4xl font-bold text-green-600">€232,000</span>
                </div>
                <div className="text-center mt-4">
                  <div className="text-sm text-gray-600">Legal Package: €499/mnd (€5,988/år)</div>
                  <div className="text-green-600 font-bold text-xl mt-2">ROI: 3,774% 🚀</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Legal Package</h2>
          <div className="max-w-md mx-auto bg-white border-4 border-slate-700 rounded-lg p-8 shadow-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-slate-700 mb-2">FOR ADVOKATFIRMAER</div>
              <div className="text-5xl font-bold mb-2">€499<span className="text-xl font-normal text-gray-600">/mnd</span></div>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">✅ Alle 10 Legal AI-agenter</li>
              <li className="flex items-center">✅ Ubegrenset dokumentanalyse</li>
              <li className="flex items-center">✅ Lovdata/case law integration</li>
              <li className="flex items-center">✅ End-to-end kryptering</li>
              <li className="flex items-center">✅ Compliance automation</li>
              <li className="flex items-center">✅ Priority support</li>
            </ul>
            <button className="w-full bg-slate-700 text-white py-4 rounded-lg font-semibold text-lg hover:bg-slate-800">
              Start 30-Dagers Gratis Prøve
            </button>
          </div>
        </div>
      </section>

      {/* Case Study */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto bg-gradient-to-r from-slate-50 to-gray-100 p-8 rounded-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-slate-700 mb-2">SUCCESS STORY</div>
              <h2 className="text-3xl font-bold mb-4">Nordisk Advokatfirma AS</h2>
              <p className="text-gray-600">Oslo • 8 advokater • Selskapsrett & M&A</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">65%</div>
                <div className="text-sm text-gray-600">Raskere kontraktreview</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">€120k</div>
                <div className="text-sm text-gray-600">Spart på junior-timer</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">100%</div>
                <div className="text-sm text-gray-600">Compliance accuracy</div>
              </div>
            </div>

            <blockquote className="border-l-4 border-slate-700 pl-4 italic text-gray-700">
              "Mindframe AI har transformert vår praksis. Vi bruker nå 70% mindre tid på dokumentgjennomgang,
              og kan fokusere på strategisk rådgivning som klientene verdsetter mest. ROI var synlig etter 2 måneder."
              <footer className="mt-2 text-sm text-gray-600">— Advokat Kari Nilsen, Partner, Nordisk Advokatfirma AS</footer>
            </blockquote>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-slate-700 to-slate-900 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Klar til å Modernisere Din Praksis?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Bli med 30+ advokatfirmaer som allerede bruker Mindframe AI.
          </p>
          <button className="bg-white text-slate-700 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
            Book Gratis Demo
          </button>
        </div>
      </section>
    </div>
  );
};

export default LegalLanding;
