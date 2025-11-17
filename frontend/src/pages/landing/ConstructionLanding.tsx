/**
 * Construction Landing Page
 * Mindframe AI for Construction & Project Management
 */
import React from 'react';

export const ConstructionLanding: React.FC = () => {
  return (
    <div className="construction-landing">
      {/* Hero */}
      <section className="hero bg-gradient-to-r from-orange-600 to-amber-600 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-sm font-semibold mb-4">🏗️ CONSTRUCTION SOLUTION</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Hold Prosjekter i Rute, Budsjett og Sikkerhet
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              AI-drevet prosjektstyring, ressursplanlegging og HMS-compliance.
              Lever 95% av prosjekter i tide og innenfor budsjett.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-orange-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
                Start Gratis Prøveperiode
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-orange-600">
                Se Demo
              </button>
            </div>
            <p className="mt-4 text-sm opacity-75">✅ BIM Integration • ✅ Safety Compliance • ✅ Real-Time Updates</p>
          </div>
        </div>
      </section>

      {/* Problem/Solution */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Utfordringer i Byggebransjen
          </h2>
          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-red-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-red-600">Problemene</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Forsinkelser:</strong> 70% av prosjekter leveres for sent</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Budsjettoverskridelser:</strong> Gjennomsnitt 15-20% over budsjett</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Dårlig kommunikasjon:</strong> 30% av tiden brukt på møter/oppklaringer</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>HMS-hendelser:</strong> 1 av 10 prosjekter har alvorlige ulykker</div>
                </li>
              </ul>
            </div>

            <div className="bg-green-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-green-600">Mindframe Løsning</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>AI tidsplanlegging:</strong> 95% leveres i tide med prediktiv analyse</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Budsjett-kontroll:</strong> Real-time tracking, 0% overraskelser</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Sentralisert info:</strong> Alt på ett sted, tilgjengelig 24/7</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Automatisk HMS:</strong> Compliance-sjekk før hver aktivitet</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Construction Agents */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            11 Spesialiserte Bygge-Agenter
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📋</div>
              <h3 className="text-xl font-bold mb-2">Project Management AI</h3>
              <p className="text-gray-600 mb-4">
                Styrer hele prosjektet. Tidsplan, milepæler, avhengigheter, risiko.
              </p>
              <div className="text-sm text-green-600 font-semibold">95% i tide</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💰</div>
              <h3 className="text-xl font-bold mb-2">Budget Tracker</h3>
              <p className="text-gray-600 mb-4">
                Sporer kostnader i sanntid. Varsler ved avvik. Predikerer sluttsum.
              </p>
              <div className="text-sm text-green-600 font-semibold">±2% nøyaktighet</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">👷</div>
              <h3 className="text-xl font-bold mb-2">Resource Allocation AI</h3>
              <p className="text-gray-600 mb-4">
                Fordeler folk, maskiner, materialer optimalt. Unngår flaskehalser.
              </p>
              <div className="text-sm text-green-600 font-semibold">30% bedre utnyttelse</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">⚠️</div>
              <h3 className="text-xl font-bold mb-2">Safety Compliance Monitor</h3>
              <p className="text-gray-600 mb-4">
                Sjekker HMS-compliance. Varsler om mangler før arbeid starter.
              </p>
              <div className="text-sm text-green-600 font-semibold">80% færre ulykker</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📦</div>
              <h3 className="text-xl font-bold mb-2">Material Procurement AI</h3>
              <p className="text-gray-600 mb-4">
                Bestiller materialer automatisk. Forhandler priser, tracker levering.
              </p>
              <div className="text-sm text-green-600 font-semibold">15% lavere kostnader</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🏗️</div>
              <h3 className="text-xl font-bold mb-2">BIM Integration Hub</h3>
              <p className="text-gray-600 mb-4">
                Integrerer med Revit, AutoCAD. Synkroniserer 3D-modeller og planer.
              </p>
              <div className="text-sm text-green-600 font-semibold">Zero model konflikter</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">✅</div>
              <h3 className="text-xl font-bold mb-2">Quality Control Inspector</h3>
              <p className="text-gray-600 mb-4">
                AI bildeanalyse av arbeid. Identifiserer feil og mangler tidlig.
              </p>
              <div className="text-sm text-green-600 font-semibold">50% færre reklamasjoner</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🌦️</div>
              <h3 className="text-xl font-bold mb-2">Weather Impact Analyzer</h3>
              <p className="text-gray-600 mb-4">
                Predikerer værforsinkelser. Justerer tidsplan automatisk.
              </p>
              <div className="text-sm text-green-600 font-semibold">Alltid oppdatert plan</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📸</div>
              <h3 className="text-xl font-bold mb-2">Progress Documentation AI</h3>
              <p className="text-gray-600 mb-4">
                Automatisk foto-dokumentasjon. Genererer fremdriftsrapporter.
              </p>
              <div className="text-sm text-green-600 font-semibold">100% dokumentert</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💬</div>
              <h3 className="text-xl font-bold mb-2">Contractor Communication Hub</h3>
              <p className="text-gray-600 mb-4">
                Sentralisert kommunikasjon. Alle underentreprenører på samme plattform.
              </p>
              <div className="text-sm text-green-600 font-semibold">90% raskere svar</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Performance Analytics</h3>
              <p className="text-gray-600 mb-4">
                Analyser produktivitet, kostnadseffektivitet, tidsbruk per aktivitet.
              </p>
              <div className="text-sm text-green-600 font-semibold">Data-drevne beslutninger</div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto bg-orange-50 p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-6 text-center">ROI-Kalkulator</h2>
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Unngåtte forsinkelser (10% av prosjekt)</span>
                  <span className="text-2xl font-bold text-green-600">€120,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Reduserte materialkostnader (15%)</span>
                  <span className="text-2xl font-bold text-green-600">€75,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Færre HMS-bøter og ulykker</span>
                  <span className="text-2xl font-bold text-green-600">€50,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Bedre ressursutnyttelse (20%)</span>
                  <span className="text-2xl font-bold text-green-600">€60,000/år</span>
                </div>
              </div>
              <div className="border-t-2 pt-6">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold">Total Årlig Verdi:</span>
                  <span className="text-4xl font-bold text-green-600">€305,000</span>
                </div>
                <div className="text-center mt-4">
                  <div className="text-sm text-gray-600">Construction Package: €349/mnd (€4,188/år)</div>
                  <div className="text-green-600 font-bold text-xl mt-2">ROI: 7,183% 🚀</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Construction Package</h2>
          <div className="max-w-md mx-auto bg-white border-4 border-orange-600 rounded-lg p-8 shadow-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-orange-600 mb-2">FOR BYGGEFIRMAER</div>
              <div className="text-5xl font-bold mb-2">€349<span className="text-xl font-normal text-gray-600">/mnd</span></div>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">✅ Alle 11 Construction AI-agenter</li>
              <li className="flex items-center">✅ Ubegrenset prosjekter</li>
              <li className="flex items-center">✅ BIM integration (Revit, AutoCAD)</li>
              <li className="flex items-center">✅ HMS compliance automation</li>
              <li className="flex items-center">✅ Real-time budsjett tracking</li>
              <li className="flex items-center">✅ Priority support</li>
            </ul>
            <button className="w-full bg-orange-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-orange-700">
              Start 30-Dagers Gratis Prøve
            </button>
          </div>
        </div>
      </section>

      {/* Case Study */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto bg-gradient-to-r from-orange-50 to-amber-50 p-8 rounded-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-orange-600 mb-2">SUCCESS STORY</div>
              <h2 className="text-3xl font-bold mb-4">Bygg & Anlegg AS</h2>
              <p className="text-gray-600">Trondheim • 50 ansatte • Boligbygg</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">100%</div>
                <div className="text-sm text-gray-600">Prosjekter levert i tide</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">€180k</div>
                <div className="text-sm text-gray-600">Spart på 3 prosjekter</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">0</div>
                <div className="text-sm text-gray-600">HMS-hendelser</div>
              </div>
            </div>

            <blockquote className="border-l-4 border-orange-600 pl-4 italic text-gray-700">
              "Mindframe AI har gitt oss full kontroll. Vi vet alltid hvor vi står på budsjett,
              vi leverer i tide, og HMS er på topp. Siste 8 prosjekter har alle vært lønnsomme - det har aldri skjedd før!"
              <footer className="mt-2 text-sm text-gray-600">— Per Johansen, Prosjektleder, Bygg & Anlegg AS</footer>
            </blockquote>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-orange-600 to-amber-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Klar til å Levere Prosjekter i Tide?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Bli med 40+ byggefirmaer som allerede bruker Mindframe AI.
          </p>
          <button className="bg-white text-orange-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
            Book Gratis Demo
          </button>
        </div>
      </section>
    </div>
  );
};

export default ConstructionLanding;
