import React, { Component } from 'react';
import './App.css';
import ImageUpload from './ImageUpload';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div class="jumbotron">
          <h1 class="display-4"> Animal Identification using Machine Learning </h1>
          <p> The purpose of this application is to display a prediction given a certain image upload.</p>
        </div>
        <ImageUpload />
      </div>
    );
  }
}

export default App;

