import React from "react";

export default function Meta({ title, description }) {
  React.useEffect(() => {
    // Update document title
    if (title) {
      document.title = title;
    }

    // Update or create meta description
    if (description) {
      let tag = document.querySelector('meta[name="description"]');
      if (!tag) {
        tag = document.createElement("meta");
        tag.setAttribute("name", "description");
        document.head.appendChild(tag);
      }
      tag.setAttribute("content", description);
    }
  }, [title, description]);

  return null; 
}
