import React from 'react';
import './App.css';
import NewsAllView from './NewsAllView';
import NewsDetailView from './NewsDetailView';
import NewsLatestView from './NewsLatestView';
import NewsSearchView from './NewsSearchView';
import NewsCategoryView from './NewsCategoryView';
import { BrowserRouter, Route } from 'react-router-dom';

class App extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Route exact path="/" component={NewsAllView} />
          <Route path="/search" component={NewsSearchView} />
          <Route path="/category" component={NewsCategoryView} />
          <Route path="/latest" component={NewsLatestView} />
          <Route path="/article/:id" component={NewsDetailView} />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
