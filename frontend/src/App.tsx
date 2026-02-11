import { useState } from 'react';
import SurveyPage from './pages/SurveyPage/SurveyPage';
import ResultPage from './pages/ResultPage/ResultPage';
import type { RecommendationResult } from './types';
import './index.css';

function App() {
  const [result, setResult] = useState<RecommendationResult | null>(null);

  const handleComplete = (data: RecommendationResult) => {
    setResult(data);
  };

  const handleRetry = () => {
    setResult(null);
  };

  return (
    <div id="app">
      {result ? (
        <ResultPage result={result} onRetry={handleRetry} />
      ) : (
        <SurveyPage onComplete={handleComplete} />
      )}
    </div>
  );
}

export default App;
