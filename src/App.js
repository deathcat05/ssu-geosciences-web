import React, { Component } from 'react';
import './App.css';
import Prediction from './Prediction';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="jumbotron">
          <h1 className="display-4"> Animal Identification using Machine Learning </h1>
          <p> The purpose of this application is to display a prediction given a certain image upload.</p>
        </div>
        <Prediction />
      </div>
    );
  }
}

export default App;

