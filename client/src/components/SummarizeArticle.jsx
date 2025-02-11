import { useState, useRef, useEffect } from 'react';

const SummarizeArticle = () => {
  const [text, setText] = useState("");
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = textareaRef.current.scrollHeight + "px";
    }
  }, [text]);

  const handleChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="rounded-xl bg-gray-800 text-gray-300 grayscale p-2 w-180">
      <textarea
        ref={textareaRef}
        value={text}
        onChange={handleChange}
        placeholder="Paste a link"
        className="w-full  text-gray-300 resize-none overflow-hidden focus:ring-0 focus:outline-none"
      >

      </textarea>
    </div>
  )
}

export default SummarizeArticle;