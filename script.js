// 获取照片展示的容器
const gallery = document.getElementById("photo-gallery");

// 定义图片文件列表
const imageFiles = [
	"images/sunrises/2025-01-01-sunrise1.JPG",
	"images/sunrises/2025-01-01-sunrise2.JPG",
	"images/sunrises/2025-01-01-sunrise3.JPG",
	"images/sunrises/IMG_3178.JPG",
	"images/sunrises/IMG_3242.JPG",
	// 未来添加新的图片时，将文件路径添加到此数组
];

// 遍历图片文件列表
imageFiles.forEach((imageFile) => {
	// 创建一个新的 Image 对象
	const img = new Image();
	img.src = imageFile;

	// 当图片加载完成后执行
	img.onload = function () {
		// 使用 EXIF 库获取图片元数据
		EXIF.getData(img, function () {
			// 获取拍摄日期信息
			let exifDate =
				EXIF.getTag(this, "DateTimeOriginal") || EXIF.getTag(this, "DateTime");

			// 如果无法获取日期，则设置为未知日期
			let displayDate = "Unknown Date";
			if (exifDate) {
				// 将日期格式从 "YYYY:MM:DD HH:MM:SS" 转换为 "YYYY-MM-DD"
				displayDate = exifDate.split(" ")[0].replace(/:/g, "-");
			}

			// 创建 figure 元素
			const figure = document.createElement("figure");

			// 创建 img 元素
			const imgElement = document.createElement("img");
			imgElement.src = imageFile;
			imgElement.alt = "Sunrise on " + displayDate;

			// 创建 figcaption 元素
			const caption = document.createElement("figcaption");
			caption.textContent = "Sunrise on " + displayDate;

			// 将 img 和 caption 添加到 figure 中
			figure.appendChild(imgElement);
			figure.appendChild(caption);

			// 将 figure 添加到展示容器中
			gallery.appendChild(figure);
		});
	};
});
