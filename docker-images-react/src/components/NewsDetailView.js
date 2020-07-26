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

const CommentViewPanel = (props) => (
  <div id="comment" class="col-md-12">
    <div class="card">
      <div class="card-header">
        <h4 class="card-title">コメント</h4>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table">
            <thead class="text-primary">
              <th>ユーザー</th>
              <th>コメント</th>
            </thead>
            <tbody>
              <tr>
                <td>名無し</td>
                <td>コメント</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
);

const CommentPostPanel = (props) => (
  <div id="comment-form" class="col-md-12">
    <div class="card card-user">
      <div class="card-header">
        <h4 class="card-title">コメントを投稿する</h4>
      </div>
      <div class="card-body">
        <form action={`/comment/${props.id}`} method="POST">
          <input type="hidden" name="news_id" value={props.id} />

          <div class="row">
            <div class="col-md-3">
              <div class="form-group">
                <label>お名前</label>
                <input type="text" name="name" class="form-control" />
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-12">
              <div class="form-group">
                <label>メッセージ</label>
                <textarea name="comment" class="form-control textarea"></textarea>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="update ml-auto mr-auto">
              <button type="submit" class="btn btn-primary btn-round">
                投稿する
              </button>
            </div>
          </div>
        </form>
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
      <>
        <div class="row">
          <NewsViewPanel
            title={item.title}
            img_url={item.img_url}
            detail={item.detail}
            updated_at={item.updated_at}
            type={item.type}
          />
        </div>
        <div class="row">
          <CommentViewPanel />
        </div>
        <div class="row">
          <CommentPostPanel id={item.id} />
        </div>
      </>
    );
  }
}

export default NewsDetailView;
