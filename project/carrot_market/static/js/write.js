function previewImage(event) {
  let reader = new FileReader();
  reader.onload = function () {
    let output = document.getElementById("imagePreview");
    output.src = reader.result;
    output.classList.add("img-upload-fit");
  };
  reader.readAsDataURL(event.target.files[0]);
}

// 테스트 중
// const fileDOM = document.querySelector('#file');
// const previews = document.querySelectorAll('.image-box');

// fileDOM.addEventListener('change', () => {
//   const reader = new FileReader();
//   reader.onload = ({ target }) => {
//     previews[0].src = target.result;
//   };
//   reader.readAsDataURL(fileDOM.files[0]);
// });
