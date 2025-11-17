/**
 * Education Landing Page
 * Mindframe AI for Schools, Universities & Online Learning
 */
import React from 'react';

export const EducationLanding: React.FC = () => {
  return (
    <div className="education-landing">
      {/* Hero */}
      <section className="hero bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-sm font-semibold mb-4">🎓 EDUCATION SOLUTION</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              AI-Drevet Utdanning som Engasjerer Studenter
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              Automatiser administrasjon, gi 24/7 studentstøtte, og personaliser læring.
              Frigjør lærere til å fokusere på undervisning.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
                Start Gratis Prøveperiode
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-purple-600">
                Se Demo
              </button>
            </div>
            <p className="mt-4 text-sm opacity-75">✅ LMS Integration • ✅ Unlimited Students • ✅ GDPR Compliant</p>
          </div>
        </div>
      </section>

      {/* Problem/Solution */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Utfordringer i Utdanningssektoren
          </h2>
          <div className="grid md:grid-cols-2 gap-12">
            <div className="bg-red-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-red-600">Problemene</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Overbelastede lærere:</strong> 40% av tiden går til administrasjon</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Sent svar til studenter:</strong> Gjennomsnitt 24-48 timer ventetid</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Høyt frafall:</strong> 30% dropper ut første året</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div><strong>Manuell retting:</strong> Timer brukt på å rette oppgaver</div>
                </li>
              </ul>
            </div>

            <div className="bg-green-50 p-8 rounded-lg">
              <h3 className="text-2xl font-bold mb-6 text-green-600">Mindframe Løsning</h3>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>AI-assistanse:</strong> Automatiser 80% av administrasjon</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>24/7 studentstøtte:</strong> Øyeblikkelige svar på spørsmål</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Personalisert læring:</strong> AI tilpasser innhold til hver student</div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div><strong>Automatisk retting:</strong> Draft feedback på sekunder</div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Education Agents */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            9 Spesialiserte Utdannings-Agenter
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">💬</div>
              <h3 className="text-xl font-bold mb-2">Student Support Chatbot</h3>
              <p className="text-gray-600 mb-4">
                Besvarer kursspørsmål 24/7. Integrert med LMS for personlige svar.
              </p>
              <div className="text-sm text-green-600 font-semibold">70% spørsmål auto-resolved</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📝</div>
              <h3 className="text-xl font-bold mb-2">Assignment Grading Helper</h3>
              <p className="text-gray-600 mb-4">
                Foreslår karakterer og gir draft feedback. Lærer godkjenner.
              </p>
              <div className="text-sm text-green-600 font-semibold">Sparer 10 timer/uke</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🎯</div>
              <h3 className="text-xl font-bold mb-2">Course Recommendation Engine</h3>
              <p className="text-gray-600 mb-4">
                Foreslår relevante kurs basert på interesse og tidligere resultater.
              </p>
              <div className="text-sm text-green-600 font-semibold">35% høyere engagement</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">✏️</div>
              <h3 className="text-xl font-bold mb-2">Enrollment Assistant</h3>
              <p className="text-gray-600 mb-4">
                Guider søkere gjennom påmeldingsprosessen. Automatisk validering.
              </p>
              <div className="text-sm text-green-600 font-semibold">90% selvbetjening</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Learning Analytics</h3>
              <p className="text-gray-600 mb-4">
                Sporer studentprogresjon. Identifiserer faresignaler tidlig.
              </p>
              <div className="text-sm text-green-600 font-semibold">15% reduksjon i frafall</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📅</div>
              <h3 className="text-xl font-bold mb-2">Attendance Tracker</h3>
              <p className="text-gray-600 mb-4">
                Automatisk fravær-registrering. Varsler foreldre ved mye fravær.
              </p>
              <div className="text-sm text-green-600 font-semibold">100% nøyaktighet</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">👨‍👩‍👧</div>
              <h3 className="text-xl font-bold mb-2">Parent Communication</h3>
              <p className="text-gray-600 mb-4">
                Sender automatiske oppdateringer om karakterer, fravær, arrangement.
              </p>
              <div className="text-sm text-green-600 font-semibold">95% fornøyde foreldre</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">📚</div>
              <h3 className="text-xl font-bold mb-2">Exam Scheduler</h3>
              <p className="text-gray-600 mb-4">
                Koordinerer eksamen-tider, rom, og tilsyn. Ingen konflikter.
              </p>
              <div className="text-sm text-green-600 font-semibold">Zero konflikter</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-3">🤖</div>
              <h3 className="text-xl font-bold mb-2">Virtual Teaching Assistant</h3>
              <p className="text-gray-600 mb-4">
                Hjelper i online klasser. Besvarer spørsmål i chat under forelesning.
              </p>
              <div className="text-sm text-green-600 font-semibold">Alltid tilgjengelig</div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto bg-purple-50 p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-6 text-center">ROI-Kalkulator</h2>
            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Lærer-tid spart (15 timer/uke)</span>
                  <span className="text-2xl font-bold text-green-600">€30,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Høyere påmelding (20% økning)</span>
                  <span className="text-2xl font-bold text-green-600">€50,000/år</span>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Redusert frafall (15%)</span>
                  <span className="text-2xl font-bold text-green-600">€40,000/år</span>
                </div>
              </div>
              <div className="border-t-2 pt-6">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold">Total Årlig Verdi:</span>
                  <span className="text-4xl font-bold text-green-600">€120,000</span>
                </div>
                <div className="text-center mt-4">
                  <div className="text-sm text-gray-600">Education Package: €199/mnd (€2,388/år)</div>
                  <div className="text-green-600 font-bold text-xl mt-2">ROI: 5,025% 🚀</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Education Package</h2>
          <div className="max-w-md mx-auto bg-white border-4 border-purple-600 rounded-lg p-8 shadow-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-purple-600 mb-2">FOR SKOLER & UNIVERSITETER</div>
              <div className="text-5xl font-bold mb-2">€199<span className="text-xl font-normal text-gray-600">/mnd</span></div>
            </div>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center">✅ Alle 9 Education AI-agenter</li>
              <li className="flex items-center">✅ Ubegrenset studenter</li>
              <li className="flex items-center">✅ LMS integrasjon (Canvas, Moodle, Blackboard)</li>
              <li className="flex items-center">✅ 24/7 studentstøtte</li>
              <li className="flex items-center">✅ Lærer-training inkludert</li>
              <li className="flex items-center">✅ Priority support</li>
            </ul>
            <button className="w-full bg-purple-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-purple-700">
              Start 30-Dagers Gratis Prøve
            </button>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Klar til å Modernisere Din Skole?</h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Bli med 100+ utdanningsinstitusjoner som allerede bruker Mindframe AI.
          </p>
          <button className="bg-white text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100">
            Book Gratis Demo
          </button>
        </div>
      </section>
    </div>
  );
};

export default EducationLanding;
