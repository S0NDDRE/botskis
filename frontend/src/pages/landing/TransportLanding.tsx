/**
 * Transport & Logistics Landing Page
 * Mindframe AI for Trucking, Delivery & Fleet Management
 */
import React from 'react';

export const TransportLanding: React.FC = () => {
  return (
    <div className="transport-landing">
      {/* Hero */}
      <section className="hero bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-sm font-semibold mb-4">🚚 TRANSPORT & LOGISTICS SOLUTION</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Optimaliser Ruter, Reduser Kostnader, Øk Lønnsomhet
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              AI-drevet flåtestyring, ruteoptimalisering og sanntidssporing.
              Spar 15% på drivstoff, lever 20% flere pakker.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
                Start Gratis Prøveperiode
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600">
                Se Demo
              </button>
            </div>
            <p className="mt-4 text-sm opacity-75">✅ GPS Integration • ✅ Real-Time Tracking • ✅ CO₂ Reporting</p>
          </div>
        </div>
      </section>

      {/* Problem/Solution */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Utfordringer i Transport & Logistikk
          </h2>
          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-red-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-red-600">Problemene</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Ineffektive ruter:</strong> 25% av kjøretid er tom-kjøring</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Høye drivstoffkostnader:</strong> 30-40% av totale utgifter</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Forsinkelser:</strong> 15% av leveranser kommer for sent</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Manuell planlegging:</strong> 5-10 timer/uke på ruteplanlegging</div>
                </li>
              </ul>
            </div>

            <div className="bg-green-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-green-600">Mindframe Løsning</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Smart ruteoptimalisering:</strong> Reduser tom-kjøring med 80%</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Drivstoffbesparelse:</strong> Spar 15% på drivstoff med AI-ruter</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Sanntidssporing:</strong> 100% sporbarhet, alltid i tide</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Automatisk planlegging:</strong> Ruter lages på sekunder</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Transport Agents */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            12 Spesialiserte Transport-Agenter
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🗺️</div>
              <h3 className="text-xl font-bold mb-2">Route Optimization AI</h3>
              <p className="text-gray-600 mb-4">
                Beregner optimale ruter med AI. Tar hensyn til trafikk, vær, prioritet.
              </p>
              <div className="text-sm text-green-600 font-semibold">15% mindre kjøretid</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🚛</div>
              <h3 className="text-xl font-bold mb-2">Fleet Management System</h3>
              <p className="text-gray-600 mb-4">
                Overvåker alle kjøretøy i sanntid. Vedlikehold, drivstoff, ytelse.
              </p>
              <div className="text-sm text-green-600 font-semibold">20% lavere vedlikehold</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📦</div>
              <h3 className="text-xl font-bold mb-2">Delivery Scheduler</h3>
              <p className="text-gray-600 mb-4">
                Planlegger leveranser automatisk. Optimaliserer for tid og kostnad.
              </p>
              <div className="text-sm text-green-600 font-semibold">30% mer kapasitet</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📍</div>
              <h3 className="text-xl font-bold mb-2">Real-Time GPS Tracker</h3>
              <p className="text-gray-600 mb-4">
                Sporer alle kjøretøy live. Kunder får nøyaktig ankomsttid.
              </p>
              <div className="text-sm text-green-600 font-semibold">100% sporbarhet</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">⛽</div>
              <h3 className="text-xl font-bold mb-2">Fuel Cost Optimizer</h3>
              <p className="text-gray-600 mb-4">
                Analyserer kjøremønster. Foreslår besparingstiltak for drivstoff.
              </p>
              <div className="text-sm text-green-600 font-semibold">€25,000/år bespart</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">👨‍✈️</div>
              <h3 className="text-xl font-bold mb-2">Driver Performance Monitor</h3>
              <p className="text-gray-600 mb-4">
                Sporer sjåfør-ytelse. Identifiserer treningsbehov og risiko.
              </p>
              <div className="text-sm text-green-600 font-semibold">40% færre ulykker</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🔧</div>
              <h3 className="text-xl font-bold mb-2">Maintenance Predictor</h3>
              <p className="text-gray-600 mb-4">
                Predikerer når kjøretøy trenger service. Unngår plutselige stans.
              </p>
              <div className="text-sm text-green-600 font-semibold">Zero nedetid</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💬</div>
              <h3 className="text-xl font-bold mb-2">Customer Notification Bot</h3>
              <p className="text-gray-600 mb-4">
                Varsler kunder automatisk om leveranser. SMS, email, push.
              </p>
              <div className="text-sm text-green-600 font-semibold">95% fornøyde kunder</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Load Optimization AI</h3>
              <p className="text-gray-600 mb-4">
                Optimaliserer lasting. Maksimerer utnyttelse av plass og vekt.
              </p>
              <div className="text-sm text-green-600 font-semibold">20% mer last per tur</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🌱</div>
              <h3 className="text-xl font-bold mb-2">Carbon Footprint Tracker</h3>
              <p className="text-gray-600 mb-4">
                Sporer CO₂-utslipp. Generer rapporter for bærekraft.
              </p>
              <div className="text-sm text-green-600 font-semibold">ESG-compliant</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📝</div>
              <h3 className="text-xl font-bold mb-2">Proof of Delivery AI</h3>
              <p className="text-gray-600 mb-4">
                Automatisk bekreftelse ved levering. Digital signatur og bilde.
              </p>
              <div className="text-sm text-green-600 font-semibold">100% dokumentasjon</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">⚠️</div>
              <h3 className="text-xl font-bold mb-2">Incident Response System</h3>
              <p className="text-gray-600 mb-4">
                Håndterer ulykker og problemer. Automatisk varsling og re-routing.
              </p>
              <div className="text-sm text-green-600 font-semibold">5 min responstid</div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto bg-blue-50 p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-6 text-center">ROI-Kalkulator</h2>
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Drivstoffbesparelse (15%)</span>
                  <span className="text-2xl font-bold text-green-600">€60,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Økt kapasitet (20% flere leveranser)</span>
                  <span className="text-2xl font-bold text-green-600">€80,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Redusert vedlikehold (20%)</span>
                  <span className="text-2xl font-bold text-green-600">€25,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Tid spart på planlegging (10t/uke)</span>
                  <span className="text-2xl font-bold text-green-600">€15,000/år</span>
                </div>
              </div>
              <div className="border-t-2 pt-6">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold">Total Årlig Verdi:</span>
                  <span className="text-4xl font-bold text-green-600">€180,000</span>
                </div>
                <div className="text-center mt-4">
                  <div className="text-sm text-gray-600">Transport Package: €399/mnd (€4,788/år)</div>
                  <div className="text-green-600 font-bold text-xl mt-2">ROI: 3,660% 🚀</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Transport Package</h2>
          <div className="max-w-md mx-auto bg-white border-4 border-blue-600 rounded-lg p-8 shadow-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-blue-600 mb-2">FOR TRANSPORT & LOGISTIKK</div>
              <div className="text-5xl font-bold mb-2">€399<span className="text-xl font-normal text-gray-600">/mnd</span></div>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">✅ Alle 12 Transport AI-agenter</li>
              <li className="flex items-center">✅ Ubegrenset kjøretøy</li>
              <li className="flex items-center">✅ GPS/Telematics integrasjon</li>
              <li className="flex items-center">✅ Sanntids ruteoptimalisering</li>
              <li className="flex items-center">✅ CO₂ rapportering</li>
              <li className="flex items-center">✅ 24/7 support</li>
            </ul>
            <button className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700">
              Start 30-Dagers Gratis Prøve
            </button>
          </div>
        </div>
      </section>

      {/* Case Study */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto bg-gradient-to-r from-blue-50 to-cyan-50 p-8 rounded-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-blue-600 mb-2">SUCCESS STORY</div>
              <h2 className="text-3xl font-bold mb-4">NorTransport AS</h2>
              <p className="text-gray-600">Bergen • 25 lastebiler • Pakkeleveranser</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">18%</div>
                <div className="text-sm text-gray-600">Drivstoffbesparelse</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">25%</div>
                <div className="text-sm text-gray-600">Flere leveranser/dag</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-green-600 mb-2">€95k</div>
                <div className="text-sm text-gray-600">Spart første året</div>
              </div>
            </div>

            <blockquote className="border-l-4 border-blue-600 pl-4 italic text-gray-700">
              "Mindframe AI ga oss full kontroll. Vi ser alt i sanntid, kundene er fornøyde,
              og vi sparer titusenvis på drivstoff hver måned. Best investering vi har gjort!"
              <footer className="mt-2 text-sm text-gray-600">— Ole Hansen, Daglig Leder, NorTransport AS</footer>
            </blockquote>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-cyan-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Klar til å Optimalisere Din Flåte?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Bli med 50+ transportselskaper som allerede bruker Mindframe AI.
          </p>
          <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
            Book Gratis Demo
          </button>
        </div>
      </section>
    </div>
  );
};

export default TransportLanding;
