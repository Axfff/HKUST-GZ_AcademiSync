document.addEventListener("DOMContentLoaded", function () {
  // 获取筛选器元素
  const semesterFilter = document.getElementById("semester-filter");
  const instructorFilter = document.getElementById("instructor-filter");
  const ratingFilter = document.getElementById("rating-filter");

  // 获取所有评价卡片
  const reviews = document.querySelectorAll(".review-card");

  // 筛选函数
  function filterReviews() {
    const selectedSemester = semesterFilter.value;
    const selectedInstructor = instructorFilter.value;
    const selectedRating = ratingFilter.value;

    reviews.forEach((review) => {
      const semester = review.querySelector(
        ".review-meta span:first-child"
      ).textContent;
      const instructor = review.querySelector(
        ".review-meta span:last-child"
      ).textContent;
      const rating = calculateAverageRating(review);

      const semesterMatch =
        selectedSemester === "all" || semester.includes(selectedSemester);
      const instructorMatch =
        selectedInstructor === "all" || instructor.includes(selectedInstructor);

      review.style.display =
        semesterMatch && instructorMatch ? "block" : "none";
    });

    // 根据评分排序
    sortReviews(selectedRating);
  }

  // 计算平均评分
  function calculateAverageRating(review) {
    const scores = review.querySelectorAll(".score-value");
    let total = 0;
    scores.forEach((score) => (total += parseFloat(score.textContent)));
    return total / scores.length;
  }

  // 排序评价
  function sortReviews(order) {
    const reviewsList = document.querySelector("ul");
    const reviewsArray = Array.from(reviews);

    reviewsArray.sort((a, b) => {
      const ratingA = calculateAverageRating(a);
      const ratingB = calculateAverageRating(b);
      return order === "high-to-low" ? ratingB - ratingA : ratingA - ratingB;
    });

    reviewsArray.forEach((review) => reviewsList.appendChild(review));
  }

  // 添加事件监听器
  semesterFilter.addEventListener("change", filterReviews);
  instructorFilter.addEventListener("change", filterReviews);
  ratingFilter.addEventListener("change", filterReviews);
});
