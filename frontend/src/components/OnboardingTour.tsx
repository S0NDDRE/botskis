/**
 * Onboarding Tour
 * Step-by-step guided tour for new users
 */
import React, { useState, useEffect } from 'react';

interface TourStep {
  id: string;
  title: string;
  description: string;
  target?: string; // CSS selector
  position?: 'top' | 'bottom' | 'left' | 'right';
  action?: {
    label: string;
    onClick: () => void;
  };
}

const tourSteps: TourStep[] = [
  {
    id: 'welcome',
    title: 'Velkommen til Mindframe AI! 🎉',
    description: 'La oss ta en rask gjennomgang av plattformen. Dette tar bare 2 minutter.',
  },
  {
    id: 'dashboard',
    title: 'Dette er Dashboardet ditt',
    description: 'Her får du oversikt over alle dine AI-agenter, statistikk og aktivitet.',
    target: '[data-tour="dashboard"]',
    position: 'bottom'
  },
  {
    id: 'agents',
    title: 'AI Agenter',
    description: 'Opprett og administrer dine AI-agenter her. Du kan lage opptil 20 agenter samtidig.',
    target: '[data-tour="agents"]',
    position: 'bottom',
    action: {
      label: 'Se agenter',
      onClick: () => (window.location.href = '/agents')
    }
  },
  {
    id: 'marketplace',
    title: 'Marketplace',
    description: 'Utforsk og installer ferdiglagde agenter fra marketplace.',
    target: '[data-tour="marketplace"]',
    position: 'bottom',
  },
  {
    id: 'create-agent',
    title: 'Opprett din første agent',
    description: 'Klar til å starte? Klikk her for å opprette din første AI-agent.',
    target: '[data-tour="create-agent"]',
    position: 'left',
    action: {
      label: 'Opprett agent',
      onClick: () => (window.location.href = '/agents/create')
    }
  },
  {
    id: 'complete',
    title: 'Du er klar! 🚀',
    description: 'Det var det! Du kan alltid starte denne guiden på nytt fra innstillinger.',
  }
];

interface OnboardingTourProps {
  isNewUser?: boolean;
  onComplete?: () => void;
}

export const OnboardingTour: React.FC<OnboardingTourProps> = ({
  isNewUser = false,
  onComplete
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const [showTour, setShowTour] = useState(false);

  useEffect(() => {
    // Check if user has completed tour before
    const hasCompletedTour = localStorage.getItem('onboarding_completed');

    if (isNewUser && !hasCompletedTour) {
      // Show tour after 1 second for new users
      setTimeout(() => setShowTour(true), 1000);
    }
  }, [isNewUser]);

  useEffect(() => {
    if (!isActive) return;

    const step = tourSteps[currentStep];
    if (step.target) {
      const element = document.querySelector(step.target);
      if (element) {
        const rect = element.getBoundingClientRect();
        const newPosition = calculatePosition(rect, step.position || 'bottom');
        setPosition(newPosition);

        // Scroll to element
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Highlight element
        element.classList.add('tour-highlight');
        return () => {
          element.classList.remove('tour-highlight');
        };
      }
    }
  }, [currentStep, isActive]);

  const calculatePosition = (rect: DOMRect, position: string) => {
    const offset = 20;
    switch (position) {
      case 'top':
        return { top: rect.top - 200, left: rect.left + rect.width / 2 - 200 };
      case 'bottom':
        return { top: rect.bottom + offset, left: rect.left + rect.width / 2 - 200 };
      case 'left':
        return { top: rect.top + rect.height / 2 - 100, left: rect.left - 420 };
      case 'right':
        return { top: rect.top + rect.height / 2 - 100, left: rect.right + offset };
      default:
        return { top: rect.bottom + offset, left: rect.left };
    }
  };

  const startTour = () => {
    setIsActive(true);
    setCurrentStep(0);
    setShowTour(false);
  };

  const nextStep = () => {
    if (currentStep < tourSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      completeTour();
    }
  };

  const previousStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const skipTour = () => {
    setIsActive(false);
    setShowTour(false);
    localStorage.setItem('onboarding_completed', 'true');
    onComplete?.();
  };

  const completeTour = () => {
    setIsActive(false);
    localStorage.setItem('onboarding_completed', 'true');
    onComplete?.();
  };

  const step = tourSteps[currentStep];
  const progress = ((currentStep + 1) / tourSteps.length) * 100;

  return (
    <>
      {/* Initial Prompt */}
      {showTour && !isActive && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md shadow-2xl">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold mb-2">Velkommen til Mindframe! 👋</h2>
              <p className="text-gray-600 mb-6">
                Vil du ha en rask omvisning? Vi viser deg de viktigste funksjonene på 2 minutter.
              </p>
              <div className="flex space-x-3">
                <button
                  onClick={skipTour}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Nei takk
                </button>
                <button
                  onClick={startTour}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Start omvisning
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tour Tooltip */}
      {isActive && (
        <>
          {/* Overlay */}
          <div className="fixed inset-0 bg-black bg-opacity-30 z-40" onClick={skipTour} />

          {/* Tooltip */}
          <div
            className="fixed z-50 bg-white rounded-lg shadow-2xl w-96 p-6"
            style={{
              top: step.target ? `${position.top}px` : '50%',
              left: step.target ? `${position.left}px` : '50%',
              transform: step.target ? 'none' : 'translate(-50%, -50%)'
            }}
          >
            {/* Progress Bar */}
            <div className="w-full h-1 bg-gray-200 rounded-full mb-4">
              <div
                className="h-1 bg-blue-600 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>

            {/* Content */}
            <div className="mb-4">
              <h3 className="text-lg font-bold mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </div>

            {/* Custom Action */}
            {step.action && (
              <button
                onClick={step.action.onClick}
                className="w-full mb-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                {step.action.label}
              </button>
            )}

            {/* Navigation */}
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                Steg {currentStep + 1} av {tourSteps.length}
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={skipTour}
                  className="text-sm text-gray-600 hover:text-gray-700"
                >
                  Hopp over
                </button>
                {currentStep > 0 && (
                  <button
                    onClick={previousStep}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    Tilbake
                  </button>
                )}
                <button
                  onClick={nextStep}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {currentStep < tourSteps.length - 1 ? 'Neste' : 'Fullfør'}
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* CSS for highlighting */}
      <style>{`
        .tour-highlight {
          position: relative;
          z-index: 45;
          box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.5);
          border-radius: 4px;
        }
      `}</style>
    </>
  );
};

export default OnboardingTour;
