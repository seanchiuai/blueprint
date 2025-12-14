import React from 'react';

const languages = [
  { name: 'English', articles: '7,102,000+' },
  { name: 'Русский', articles: '2 074 000+' },
  { name: 'Français', articles: '2,724,000+' },
  { name: '中文', articles: '1,514,000+' },
  { name: 'Polski', articles: '1 677 000+' },
  { name: '日本語', articles: '1,483,000+' },
  { name: 'Deutsch', articles: '3.075.000+' },
  { name: 'Español', articles: '2.078.000+' },
  { name: 'Italiano', articles: '1.947.000+' },
  { name: 'Português', articles: '1.161.000+' },
];

const sisterProjects = [
  { name: 'Commons', description: 'Free media collection' },
  { name: 'Wikibooks', description: 'Free textbooks' },
  { name: 'Wikiversity', description: 'Free learning resources' },
  { name: 'Wikivoyage', description: 'Free travel guide' },
  { name: 'Wikinews', description: 'Free news source' },
  { name: 'Wikiquote', description: 'Free quote compendium' },
];

const LandingPage: React.FC = () => {
  return (
    <div className="dark:bg-gray-900 dark:text-white transition-colors duration-300 min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md py-4 px-6">
        <div className="container mx-auto flex items-center justify-between">
          <a href="#" className="text-2xl font-bold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors duration-200">
            Wikipedia
          </a>
          <div className="flex items-center space-x-4">
            <select
              aria-label="Select language"
              className="border rounded px-2 py-1 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            >
              <option>EN</option>
              {/* Add more language options here */}
            </select>
            <button aria-label="Search" className="bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full p-2 transition-colors duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto py-12 px-6 flex flex-col lg:flex-row gap-8">
        <div className="lg:w-2/3">
          <h1 className="text-4xl font-extrabold text-gray-800 dark:text-gray-100 mb-6">
            Welcome to Wikipedia,
            <br className="hidden sm:block" />
            The Free Encyclopedia
          </h1>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {languages.map((lang) => (
              <a
                key={lang.name}
                href="#"
                className="block p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 bg-white dark:bg-gray-800 dark:border dark:border-gray-700"
                aria-label={`View Wikipedia in ${lang.name}`}
              >
                <h2 className="text-lg font-semibold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors duration-200">
                  {lang.name}
                </h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">{lang.articles} articles</p>
              </a>
            ))}
          </div>
          <button className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-200">
            Read Wikipedia in your language
          </button>
        </div>

        {/* Donation Callout */}
        <div className="lg:w-1/3 bg-yellow-100 dark:bg-yellow-800 rounded-lg shadow-md p-6 flex flex-col items-center">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4 text-center">
            We rely on your support!
          </h2>
          <p className="text-gray-700 dark:text-gray-300 text-center mb-6">
            To protect our independence, we'll never run ads. We survive on donations averaging about $15. Only a tiny portion of our readers give. If everyone reading this right now gave $3, our fundraiser would be finished within an hour.
          </p>
          <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-200 mb-2">
            Donate Now
          </button>
          <button className="text-blue-500 hover:text-blue-700 dark:text-blue-300 dark:hover:text-blue-100 transition-colors duration-200">I already donated</button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 dark:bg-gray-800 py-6 px-6 mt-auto">
        <div className="container mx-auto">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4">Sister Projects:</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {sisterProjects.map((project) => (
              <div key={project.name} className="flex items-center space-x-2">
                {/* Replace with actual icons */}
                <span className="text-gray-500 dark:text-gray-400">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z" />
                    <path fillRule="evenodd" d="M3 8a2 2 0 012-2h10a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5.5 3.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" clipRule="evenodd" />
                  </svg>
                </span>
                <div>
                  <h4 className="text-gray-700 dark:text-gray-300">{project.name}</h4>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{project.description}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 text-center text-gray-500 dark:text-gray-400">
            &copy; {new Date().getFullYear()} Wikipedia &bull; <a href="#" className="hover:underline">Terms of Use</a> &bull; <a href="#" className="hover:underline">Privacy Policy</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;