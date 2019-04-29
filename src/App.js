import React, { Component } from 'react';
import './App.css';
import Prediction from './Prediction';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="jumbotron">
          <h1 className="display-4 bg-transparent"> Sigma Clast Recognition using Transfer Learning </h1>
          <p id="purpose"> Identifying geostones with a trained convolutional neural network</p>
        </div>
        <Prediction />
      </div>
    );
  }
}

export default App;

