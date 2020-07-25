import React from 'react';
import './App.css';

const NewsViewPanel = (props) => (
  <div id="article" class="col-md-12">
    <div class="card ">
      <div class="card-header ">
        <h4 class="card-title">{props.title}</h4>
      </div>
      <div class="card-body ">
        <img src={props.img_url} alt={props.title}></img>
        <div
          dangerouslySetInnerHTML={{
            __html: props.detail,
          }}
        />
      </div>
      <div class="card-footer ">
        <hr></hr>
        <div class="stats">
          <i class="fa fa-history"></i> {props.updated_at}
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
        />
      </div>
    );
  }
}

export default NewsDetailView;
