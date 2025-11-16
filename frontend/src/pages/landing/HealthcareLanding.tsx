/**
 * Healthcare Industry Landing Page
 * Mindframe AI for Healthcare - HIPAA Compliant
 */
import React from 'react';

export const HealthcareLanding: React.FC = () => {
  return (
    <div className="healthcare-landing">
      {/* Hero Section */}
      <section className="hero bg-gradient-to-r from-blue-500 to-teal-500 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-sm font-semibold mb-4">🏥 HEALTHCARE SOLUTION</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              AI-Drevet Helsevesen som Prioriterer Pasienter
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              Reduser ventetider, automatiser timebestilling, og gi pasienter 24/7 support.
              HIPAA-compliant og trygt for sensitive helsedata.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition">
                Start Gratis Prøveperiode
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition">
                Se Demo
              </button>
            </div>
            <p className="mt-4 text-sm opacity-75">✅ HIPAA Compliant • ✅ GDPR Compliant • ✅ 99.9% Uptime</p>
          </div>
        </div>
      </section>

      {/* Problem/Solution */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold mb-6 text-red-600">Utfordringer i Helsevesenet</h2>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div>
                    <strong>Lange ventetider:</strong> Pasienter venter i gjennomsnitt 2-4 timer på svar
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div>
                    <strong>Overbelastet personale:</strong> Sykepleiere bruker 60% av tiden på administrasjon
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div>
                    <strong>Manglende oppfølging:</strong> 40% av pasienter glemmer oppfølgingsavtaler
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">❌</span>
                  <div>
                    <strong>Manuell journalføring:</strong> Legger tar timer på dokumentasjon hver dag
                  </div>
                </li>
              </ul>
            </div>

            <div className="bg-green-50 p-8 rounded-lg">
              <h2 className="text-3xl font-bold mb-6 text-green-600">Mindframe AI Løsning</h2>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <strong>Øyeblikkelig respons:</strong> AI-agent svarer pasienter på 2 minutter
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <strong>Automatisert booking:</strong> Tidsbestilling uten menneskelig inngripen
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <strong>Smart påminnelser:</strong> SMS/Email 24h før time reduserer no-shows med 80%
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-2xl mr-3">✅</span>
                  <div>
                    <strong>AI-assistert journalføring:</strong> Automatisk generering av journalnotater
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Healthcare Agents */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            11 Spesialiserte Helsevesen-Agenter
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">📅</div>
              <h3 className="text-xl font-bold mb-2">Timebestilling-Agent</h3>
              <p className="text-gray-600 mb-4">
                Automatisk booking, rebooking, og kansellering. Integrasjon med eksisterende systemer.
              </p>
              <div className="text-sm text-green-600 font-semibold">Sparer 15 timer/uke</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">💊</div>
              <h3 className="text-xl font-bold mb-2">Resept-Fornyelse</h3>
              <p className="text-gray-600 mb-4">
                Automatisk behandling av reseptforespørsler. Varsler lege ved behov.
              </p>
              <div className="text-sm text-green-600 font-semibold">80% automatisert</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">🩺</div>
              <h3 className="text-xl font-bold mb-2">Symptom-Sjekk</h3>
              <p className="text-gray-600 mb-4">
                Førstelinjes vurdering. Triagerer pasienter til riktig akuttgrad.
              </p>
              <div className="text-sm text-green-600 font-semibold">Reduserer unødvendige besøk</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">📋</div>
              <h3 className="text-xl font-bold mb-2">Journal-Assistent</h3>
              <p className="text-gray-600 mb-4">
                Lytter til konsultasjoner og genererer journalnotater automatisk.
              </p>
              <div className="text-sm text-green-600 font-semibold">Sparer 2 timer/dag</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">🔔</div>
              <h3 className="text-xl font-bold mb-2">Pasient-Påminnelser</h3>
              <p className="text-gray-600 mb-4">
                Automatiske påminnelser om timer, medisinering, og oppfølging.
              </p>
              <div className="text-sm text-green-600 font-semibold">80% færre no-shows</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">📞</div>
              <h3 className="text-xl font-bold mb-2">24/7 Pasientstøtte</h3>
              <p className="text-gray-600 mb-4">
                Besvarer vanlige spørsmål, gir helseinformasjon, eskalerer ved behov.
              </p>
              <div className="text-sm text-green-600 font-semibold">Alltid tilgjengelig</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">🧪</div>
              <h3 className="text-xl font-bold mb-2">Prøvesvar-Varsling</h3>
              <p className="text-gray-600 mb-4">
                Informerer pasienter om prøveresultater. Bestiller time ved avvik.
              </p>
              <div className="text-sm text-green-600 font-semibold">Raskere oppfølging</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">💰</div>
              <h3 className="text-xl font-bold mb-2">Fakturering</h3>
              <p className="text-gray-600 mb-4">
                Automatisk generering av regninger, purringer, og betalingsoppfølging.
              </p>
              <div className="text-sm text-green-600 font-semibold">99% nøyaktighet</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Kvalitets-Rapportering</h3>
              <p className="text-gray-600 mb-4">
                Automatisk samling av kvalitetsdata for rapportering til helsetilsynet.
              </p>
              <div className="text-sm text-green-600 font-semibold">100% compliance</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">🏥</div>
              <h3 className="text-xl font-bold mb-2">Innleggelse-Koordinering</h3>
              <p className="text-gray-600 mb-4">
                Koordinerer sykehusinnleggelser, forbereder papirer, informerer pasient.
              </p>
              <div className="text-sm text-green-600 font-semibold">Sømløs overgang</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm hover:shadow-lg transition">
              <div className="text-4xl mb-3">📱</div>
              <h3 className="text-xl font-bold mb-2">Telemedisinske Konsultasjoner</h3>
              <p className="text-gray-600 mb-4">
                Setter opp og forbereder videokonsultasjoner. Tester teknologi på forhånd.
              </p>
              <div className="text-sm text-green-600 font-semibold">95% success rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI Calculator */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto bg-blue-50 p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-6 text-center">ROI-Kalkulator: Din Besparelse</h2>

            <div className="space-y-6">
              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold">Redusert administrasjonstid</span>
                  <span className="text-2xl font-bold text-green-600">20 timer/uke</span>
                </div>
                <div className="text-sm text-gray-600">
                  À €50/time = <strong>€52,000/år</strong>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold">Færre no-shows (80% reduksjon)</span>
                  <span className="text-2xl font-bold text-green-600">€30,000/år</span>
                </div>
                <div className="text-sm text-gray-600">
                  Basert på 10 tapte timer/uke à €200/time
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold">Økt pasientkapasitet (15%)</span>
                  <span className="text-2xl font-bold text-green-600">€75,000/år</span>
                </div>
                <div className="text-sm text-gray-600">
                  Flere pasienter = mer inntekt
                </div>
              </div>

              <div className="border-t-2 pt-6 mt-6">
                <div className="flex justify-between items-center">
                  <span className="text-xl font-bold">Total Årlig Besparelse:</span>
                  <span className="text-4xl font-bold text-green-600">€157,000</span>
                </div>
                <div className="text-center mt-4">
                  <div className="text-sm text-gray-600">Mindframe AI Healthcare Package:</div>
                  <div className="text-2xl font-bold">€299/måned (€3,588/år)</div>
                  <div className="text-green-600 font-bold text-xl mt-2">
                    ROI: 4,275% 🚀
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Compliance */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Trygghet & Compliance
          </h2>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow text-center">
              <div className="text-5xl mb-4">🔒</div>
              <h3 className="text-xl font-bold mb-3">HIPAA Compliant</h3>
              <p className="text-gray-600">
                Alle pasientdata krypteres og lagres i henhold til HIPAA-krav.
                Ingen tredjeparter får tilgang.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow text-center">
              <div className="text-5xl mb-4">🇪🇺</div>
              <h3 className="text-xl font-bold mb-3">GDPR Compliant</h3>
              <p className="text-gray-600">
                Full kontroll over persondata. Rett til innsyn, sletting, og portabilitet.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow text-center">
              <div className="text-5xl mb-4">🏥</div>
              <h3 className="text-xl font-bold mb-3">Helsetilsynet-Godkjent</h3>
              <p className="text-gray-600">
                Oppfyller norske krav for journalføring og pasientbehandling.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Case Study */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-gradient-to-r from-blue-500 to-teal-500 text-white p-8 rounded-lg">
              <div className="text-sm font-semibold mb-2">SUKSESSHISTORIE</div>
              <h2 className="text-3xl font-bold mb-6">
                Oslo Helseklinikk: Fra Kaos til Kontroll på 30 Dager
              </h2>

              <div className="grid md:grid-cols-3 gap-6 mb-6">
                <div>
                  <div className="text-4xl font-bold mb-2">92%</div>
                  <div className="text-sm opacity-90">Færre telefonhenvendelser</div>
                </div>
                <div>
                  <div className="text-4xl font-bold mb-2">€8,000</div>
                  <div className="text-sm opacity-90">Månedlig besparelse</div>
                </div>
                <div>
                  <div className="text-4xl font-bold mb-2">4.8/5</div>
                  <div className="text-sm opacity-90">Pasiettilfredshet (opp fra 3.2)</div>
                </div>
              </div>

              <blockquote className="border-l-4 border-white pl-4 italic">
                "Vi var skeptiske, men Mindframe AI forandret vår hverdag fullstendig.
                Resepsjonen er ikke lenger overbelastet, pasienter får svar øyeblikkelig,
                og legene kan fokusere på det de er best til - å behandle pasienter."
              </blockquote>
              <div className="mt-4">
                <strong>- Dr. Anne Kristiansen</strong>
                <div className="text-sm opacity-75">Leder, Oslo Helseklinikk</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Healthcare Package
          </h2>

          <div className="max-w-md mx-auto bg-white border-4 border-blue-600 rounded-lg p-8 shadow-lg">
            <div className="text-center mb-6">
              <div className="text-sm font-semibold text-blue-600 mb-2">KOMPLETT LØSNING</div>
              <div className="text-5xl font-bold mb-2">€299<span className="text-xl font-normal text-gray-600">/mnd</span></div>
              <div className="text-gray-600">Alt inkludert</div>
            </div>

            <ul className="space-y-3 mb-8">
              <li className="flex items-center">✅ Alle 11 Healthcare AI-agenter</li>
              <li className="flex items-center">✅ Ubegrenset pasienter</li>
              <li className="flex items-center">✅ HIPAA & GDPR compliant</li>
              <li className="flex items-center">✅ Journal-integrasjon (EPJ)</li>
              <li className="flex items-center">✅ 24/7 priority support</li>
              <li className="flex items-center">✅ Norsk kundeservice</li>
              <li className="flex items-center">✅ Opplæring inkludert</li>
              <li className="flex items-center">✅ Ingen bindingstid</li>
            </ul>

            <button className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 transition mb-4">
              Start 30-Dagers Gratis Prøveperiode
            </button>

            <p className="text-center text-sm text-gray-600">
              Intet kredittkort påkrevd • Kanseller når som helst
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-blue-500 to-teal-500 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Klar til å Revolusjonere Din Helseklinikk?
          </h2>
          <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
            Bli med 50+ helseklinikker som allerede sparer tid og penger med Mindframe AI.
          </p>
          <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition">
            Book Gratis Demo
          </button>
        </div>
      </section>
    </div>
  );
};

export default HealthcareLanding;
