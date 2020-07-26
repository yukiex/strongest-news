import React from 'react';
import './App.css';
import NewsPanel from './NewsPanel';
import queryString from 'query-string';

class NewsCategoryView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      items: [],
    };
  }
  componentDidMount() {
    const values = queryString.parse(this.props.location.search);
    fetch(`/category?type=${values.type}`)
      .then((res) => res.json())
      .then(
        (json) => {
          console.log(json);
          this.setState({
            isLoaded: true,
            items: json,
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
    return (
      <div class="row">
        {this.state.items.map((item) => (
          <NewsPanel title={item.title} img_url={item.img_url} page_url={item.id} />
        ))}
      </div>
    );
  }
}

export default NewsCategoryView;
