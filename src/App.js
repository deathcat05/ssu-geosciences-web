import React, { Component } from 'react';
import './App.css';
import Prediction from './Prediction';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="jumbotron">
          <h1 className="display-4"> Sigma Clast Recoginition using Transfer Leanring </h1>
          <p> The purpose of this application is to display whether a stone contains a sigma clast or not.</p>
        </div>
        <Prediction />
      </div>
    );
  }
}

export default App;

