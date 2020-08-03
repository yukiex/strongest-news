import React from 'react';
import './App.css';

const NewsPanel = (props) => (
  <div className="col-md-4">
    <a href={`/article/${props.page_url}`}>
      <div className="card">
        <div className="card-header">
          <p className="card-title">{props.title}</p>
        </div>
        <div className="card-body">
          <img
            className="d-block mx-auto"
            style={{ height: '200px' }}
            src={`${props.img_url}`}
            onError={(e) => (e.target.src = '/img/noimage.png')}
            alt={`${props.title}`}
          />
        </div>
        <div className="card-footer">
          <hr></hr>
          <div className="stats">続きを読む</div>
        </div>
      </div>
    </a>
  </div>
);

export default NewsPanel;
