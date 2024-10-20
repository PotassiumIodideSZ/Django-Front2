const TabSelector = ({ activeTab }) => {
  const handleTabChange = (tab) => {
    if (tab === "dataProcessing") {
      window.location.href = "/";
    } else if (tab === "categoryKeywords") {
      window.location.href = "/category-edit";
    } else if (tab === "emailCampaign") {
      window.location.href = "/email-campaign"; // Новый маршрут для рассылки по почте
    }
  };

  return (
    <div class="tab-selector">
      <button
        onClick={() => handleTabChange("dataProcessing")}
        className={`button ${
          activeTab === "dataProcessing" ? "button--active" : "button--inactive"
        }`}
      >
        Обработка данных
      </button>
      <button
        onClick={() => handleTabChange("categoryKeywords")}
        className={`button ${
          activeTab === "categoryKeywords"
            ? "button--active"
            : "button--inactive"
        }`}
      >
        Изменение категорий и ключевых слов
      </button>
      <button
        onClick={() => handleTabChange("emailCampaign")}
        className={`button ${
          activeTab === "emailCampaign" ? "button--active" : "button--inactive"
        }`}
      >
        Рассылка по почте
      </button>
    </div>
  );
};

export default TabSelector;
