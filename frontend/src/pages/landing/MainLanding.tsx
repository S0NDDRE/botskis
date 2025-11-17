/**
 * Main Landing Page
 * Mindframe AI - Complete AI Agent Marketplace
 */
import React from 'react';

export const MainLanding: React.FC = () => {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Transform Your Business with AI Agents
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              57 AI-powered agents ready to automate, optimize, and accelerate your operations.
              From customer support to predictive analytics - we've got you covered.
            </p>
            <div className="flex flex-col md:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition">
                Start Free Trial
              </button>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-12 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-center items-center gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600">57</div>
              <div className="text-gray-600">AI Agents</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600">6</div>
              <div className="text-gray-600">Industries</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600">7</div>
              <div className="text-gray-600">Languages</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600">450%</div>
              <div className="text-gray-600">Avg ROI</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Why Choose Mindframe AI?
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-2xl font-bold mb-3">57 Ready-Made Agents</h3>
              <p className="text-gray-600">
                Customer support, sales, analytics, content creation, and more.
                Activate in seconds, customize in minutes.
              </p>
            </div>

            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-2xl font-bold mb-3">R-Learning Technology</h3>
              <p className="text-gray-600">
                Our agents learn from every interaction. Performance improves from
                50% to 92% success rate over time.
              </p>
            </div>

            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">🌍</div>
              <h3 className="text-2xl font-bold mb-3">Multi-Language Support</h3>
              <p className="text-gray-600">
                Norwegian, Swedish, Danish, Finnish, German, British & American English.
                Perfect for Nordic & European markets.
              </p>
            </div>

            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-2xl font-bold mb-3">Predictive Analytics</h3>
              <p className="text-gray-600">
                AI-powered sales forecasting, churn prediction, and lead scoring.
                Make data-driven decisions with confidence.
              </p>
            </div>

            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-2xl font-bold mb-3">Enterprise Security</h3>
              <p className="text-gray-600">
                GDPR, HIPAA, and PCI-DSS compliant. Self-hosted options available.
                Your data, your control.
              </p>
            </div>

            <div className="p-6 border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-2xl font-bold mb-3">Lightning Fast Setup</h3>
              <p className="text-gray-600">
                No coding required. Activate agents with one click.
                Integrate with your existing systems via API.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Industries */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Tailored Solutions for Your Industry
          </h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <a href="/landing/healthcare" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">🏥</div>
              <h3 className="text-xl font-bold mb-2">Healthcare</h3>
              <p className="text-gray-600">Patient support, appointment scheduling, medical records management</p>
            </a>

            <a href="/landing/education" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">🎓</div>
              <h3 className="text-xl font-bold mb-2">Education</h3>
              <p className="text-gray-600">Student support, grading assistance, course recommendations</p>
            </a>

            <a href="/landing/transport" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">🚚</div>
              <h3 className="text-xl font-bold mb-2">Transport & Logistics</h3>
              <p className="text-gray-600">Route optimization, fleet management, customer updates</p>
            </a>

            <a href="/landing/legal" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">⚖️</div>
              <h3 className="text-xl font-bold mb-2">Legal Services</h3>
              <p className="text-gray-600">Document analysis, case research, client intake</p>
            </a>

            <a href="/landing/construction" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">🏗️</div>
              <h3 className="text-xl font-bold mb-2">Construction</h3>
              <p className="text-gray-600">Project management, safety monitoring, equipment tracking</p>
            </a>

            <a href="/landing/hospitality" className="block p-6 bg-white border rounded-lg hover:shadow-lg transition">
              <div className="text-4xl mb-3">🏨</div>
              <h3 className="text-xl font-bold mb-2">Hospitality</h3>
              <p className="text-gray-600">Booking management, guest support, review responses</p>
            </a>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Simple, Transparent Pricing
          </h2>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="border rounded-lg p-8 hover:shadow-lg transition">
              <h3 className="text-2xl font-bold mb-4">Starter</h3>
              <div className="text-4xl font-bold mb-6">€49<span className="text-lg font-normal text-gray-600">/mo</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">✅ 5 AI Agents</li>
                <li className="flex items-center">✅ 1,000 requests/month</li>
                <li className="flex items-center">✅ Email support</li>
                <li className="flex items-center">✅ Basic analytics</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
                Start Free Trial
              </button>
            </div>

            <div className="border-4 border-blue-600 rounded-lg p-8 hover:shadow-lg transition relative">
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                MOST POPULAR
              </div>
              <h3 className="text-2xl font-bold mb-4">Professional</h3>
              <div className="text-4xl font-bold mb-6">€199<span className="text-lg font-normal text-gray-600">/mo</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">✅ 20 AI Agents</li>
                <li className="flex items-center">✅ 10,000 requests/month</li>
                <li className="flex items-center">✅ Priority support</li>
                <li className="flex items-center">✅ Advanced analytics</li>
                <li className="flex items-center">✅ API access</li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition">
                Start Free Trial
              </button>
            </div>

            <div className="border rounded-lg p-8 hover:shadow-lg transition">
              <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
              <div className="text-4xl font-bold mb-6">Custom</div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">✅ All 57 AI Agents</li>
                <li className="flex items-center">✅ Unlimited requests</li>
                <li className="flex items-center">✅ 24/7 support</li>
                <li className="flex items-center">✅ Custom integrations</li>
                <li className="flex items-center">✅ Self-hosted option</li>
              </ul>
              <button className="w-full border-2 border-blue-600 text-blue-600 py-3 rounded-lg font-semibold hover:bg-blue-600 hover:text-white transition">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Trusted by Leading Companies
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="text-yellow-400 text-xl">★★★★★</div>
              </div>
              <p className="text-gray-700 mb-4">
                "Mindframe AI reduced our customer support costs by 60% while improving
                response time from 2 hours to 2 minutes. Game changer!"
              </p>
              <div className="font-semibold">Lars Hansen</div>
              <div className="text-gray-600 text-sm">CEO, TechNorway AS</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="text-yellow-400 text-xl">★★★★★</div>
              </div>
              <p className="text-gray-700 mb-4">
                "The predictive sales engine helped us identify high-value leads.
                We closed 3x more deals in Q1!"
              </p>
              <div className="font-semibold">Emma Svensson</div>
              <div className="text-gray-600 text-sm">Sales Director, Stockholm Ventures</div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <div className="text-yellow-400 text-xl">★★★★★</div>
              </div>
              <p className="text-gray-700 mb-4">
                "GDPR compliance was our biggest concern. Mindframe's self-hosted option
                gave us complete control. Perfect!"
              </p>
              <div className="font-semibold">Klaus Müller</div>
              <div className="text-gray-600 text-sm">CTO, Berlin Healthcare GmbH</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join hundreds of companies using Mindframe AI to automate and accelerate.
          </p>
          <div className="flex flex-col md:flex-row gap-4 justify-center">
            <button className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition">
              Start 14-Day Free Trial
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition">
              Schedule a Demo
            </button>
          </div>
          <p className="mt-4 text-sm opacity-75">No credit card required • Cancel anytime</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">Mindframe AI</h3>
              <p className="text-gray-400">
                Empowering businesses with intelligent automation.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/features" className="hover:text-white">Features</a></li>
                <li><a href="/pricing" className="hover:text-white">Pricing</a></li>
                <li><a href="/agents" className="hover:text-white">AI Agents</a></li>
                <li><a href="/integrations" className="hover:text-white">Integrations</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/about" className="hover:text-white">About Us</a></li>
                <li><a href="/blog" className="hover:text-white">Blog</a></li>
                <li><a href="/careers" className="hover:text-white">Careers</a></li>
                <li><a href="/contact" className="hover:text-white">Contact</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/privacy" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="/terms" className="hover:text-white">Terms of Service</a></li>
                <li><a href="/security" className="hover:text-white">Security</a></li>
                <li><a href="/gdpr" className="hover:text-white">GDPR</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2025 Mindframe AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default MainLanding;
