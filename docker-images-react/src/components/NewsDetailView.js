import React from 'react';
import './App.css';

const NewsViewPanel = (props) => (
  <div id="article" className="col-md-12">
    <div className="card ">
      <div className="card-header ">
        <h4 className="card-title">{props.title}</h4>
        <p className="card-category">カテゴリー：{props.type}</p>
      </div>
      <div className="card-body ">
        <div className="article_img">
          <img src={props.img_url} alt={props.title}></img>
        </div>
        <div
          dangerouslySetInnerHTML={{
            __html: props.detail,
          }}
        />
      </div>
      <div className="card-footer ">
        <hr></hr>
        <div className="stats">
          <i className="fa fa-history"></i> {props.updated_at}
        </div>
      </div>
    </div>
  </div>
);

class NewsDetailView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      item: [],
    };
  }
  componentDidMount() {
    const { params } = this.props.match;
    fetch(`/article/${params.id}`)
      .then((res) => res.json())
      .then(
        (json) => {
          console.log(json);
          this.setState({
            isLoaded: true,
            item: json,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }
  render() {
    const item = this.state.item;
    return (
      <div class="row">
        <NewsViewPanel
          title={item.title}
          img_url={item.img_url}
          detail={item.detail}
          updated_at={item.updated_at}
          type={item.type}
        />
      </div>
    );
  }
}

export default NewsDetailView;
