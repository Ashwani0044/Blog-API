import { useState } from "react";
import API from "../api/api";

export default function CreatePost() {
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");

  const handleGenerateCaption = async () => {
    try {
      const res = await API.post("/ai/generate-caption", {
        content: content,
      });
      setTitle(res.data.caption);
    } catch (err) {
      alert("AI error");
    }
  };

  const handleCreatePost = async () => {
    try {
      await API.post("/posts", {
        title: title,
        content: content,
      });
      alert("Post created");
      setTitle("");
      setContent("");
    } catch (err) {
      alert("Error creating post");
    }
  };

  return (
    <div>
      <h2>Create Post</h2>

      <textarea
        placeholder="Write your content..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <br />

      <input
        placeholder="Caption (AI will fill)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <br />

      <button onClick={handleGenerateCaption}>
        Generate Caption
      </button>

      <button onClick={handleCreatePost}>
        Create Post
      </button>
    </div>
  );
}