document.addEventListener('DOMContentLoaded', () => {
  const addTagButton = document.querySelector('.add-tag');
  const tagsContainer = document.getElementById('tags-container');
  // 图片上传相关
  const uploadButton = document.querySelector('.upload-button');
  const fileInput = document.getElementById('file-input');
  const imagePreview = document.querySelector('.image-preview');
  const imagesData = []; // 存储图片数据

  uploadButton.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', handleFileSelect);

  function handleFileSelect(e) {
      const files = e.target.files;
      for (const file of files) {
          if (!file.type.startsWith('image/')) continue;
          
          const reader = new FileReader();
          reader.onload = (event) => {
              const img = document.createElement('img');
              img.src = event.target.result;
              img.classList.add('preview-image');
              imagePreview.appendChild(img);
              imagesData.push(event.target.result); // 存储Base64数据
          };
          reader.readAsDataURL(file);
      }
  }
  let isTagInputVisible = false; // 用于检查输入框是否已经显示

  addTagButton.addEventListener('click', () => {
    // 如果已有输入框，则不再显示新输入框
    if (isTagInputVisible) return;

    const tagInput = document.createElement('input');
    tagInput.type = 'text';
    tagInput.placeholder = 'Enter a tag';
    tagInput.classList.add('tag-input-field');
    
    tagsContainer.appendChild(tagInput);
    
    tagInput.focus();
    isTagInputVisible = true; // 显示输入框后标记为true

    tagInput.addEventListener('blur', () => createTag(tagInput));

    // 使用事件委托，在按下回车键时创建标签
    tagInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault(); // 阻止回车键的默认行为，避免触发blur事件
        // createTag(tagInput);
        e.target.blur();
      }
    });
  });

  function createTag(inputElement) {
    if (inputElement.value.trim() !== '') {
      const tag = document.createElement('div');
      tag.classList.add('tag');
      tag.textContent = '# ' + inputElement.value;
      
      // 点击标签进行编辑
      tag.addEventListener('click', () => editTag(tag));

      tagsContainer.appendChild(tag);
    }
    
    inputElement.remove(); // 移除输入框
    isTagInputVisible = false; // 隐藏输入框，允许再次点击“Add Tag”添加新标签
  }

  function editTag(tagElement) {
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.value = tagElement.textContent;
    inputField.classList.add('tag-input-field');
    
    tagsContainer.appendChild(inputField);
    
    inputField.focus();

    // 当输入框失去焦点或用户按下回车时，更新标签
    
    inputField.addEventListener('keypress', (e) => {
      inputField.addEventListener('blur', () => updateTag(inputField, tagElement));
      if (e.key === 'Enter') {
        //  阻止回车键的默认行为，避免触发blur事件
        e.preventDefault();
        e.target.blur();
        updateTag(inputField, tagElement);
      }
    });
    
  }

  function updateTag(inputElement, tagElement) {
    if (inputElement.value.trim() !== '') {
      tagElement.textContent = inputElement.value;
    }
    inputElement.remove(); // 移除输入框
  }

  document.querySelector('.submit-post').addEventListener('click', () => {
    const postData = {
        title: document.getElementById('title').value,
        tags: Array.from(document.querySelectorAll('.tag')).map(tag => tag.textContent.slice(1)),
        content: document.getElementById('content').value,
        images: imagesData
    };
    console.log('提交的数据:', postData);
    // 这里可以添加实际的提交逻辑
    alert('Post submitted with ' + imagesData.length + ' images!');
  });
});
