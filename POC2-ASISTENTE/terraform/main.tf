# 1. GRUPO DE RECURSOS
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# 2. ALMACENAMIENTO (Capa Gratuita/Económica)
resource "azurerm_storage_account" "st" {
  # Azure no permite guiones en nombres de storage, por eso usamos replace
  name                     = "st${replace(var.project_name, "-", "")}${var.environment}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# 3. OBSERVABILIDAD (Insights + Logs)
resource "azurerm_log_analytics_workspace" "logs" {
  name                = "log-${var.project_name}-workspace"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "PerGB2018"
}

resource "azurerm_application_insights" "insights" {
  name                = "appi-${var.project_name}-assistant"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  workspace_id        = azurerm_log_analytics_workspace.logs.id
  application_type    = "web"
}

# 4. SERVICIO DE BÚSQUEDA (RAG - Capa Free)
resource "azurerm_search_service" "search" {
  name                = "srch-${var.project_name}-rag"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "free"
}

# 5. BASE DE DATOS SQL (Capa Basic)
resource "azurerm_mssql_server" "sql" {
  name                         = "sql-${var.project_name}-server"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = "admincley"
  administrator_login_password = var.sql_admin_password
}

resource "azurerm_mssql_database" "db" {
  name      = "db-cley-inventory"
  server_id = azurerm_mssql_server.sql.id
  sku_name  = "Basic"
}

# 6. PLAN DE SERVICIO (Consumption / Serverless)
resource "azurerm_service_plan" "plan" {
  name                = "plan-${var.project_name}-assistant"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

# 7. LA FUNCTION APP (Configuración que enviaste)
resource "azurerm_linux_function_app" "app_engine" {
  name                = "func-${var.project_name}-assistant"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.st.name
  storage_account_access_key = azurerm_storage_account.st.primary_access_key
  service_plan_id            = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      python_version = "3.11" 
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.insights.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.insights.connection_string
    "AZURE_SEARCH_ENDPOINT"                 = "https://${azurerm_search_service.search.name}.search.windows.net"
    "AZURE_SEARCH_KEY"                      = azurerm_search_service.search.primary_key
    "AZURE_SEARCH_INDEX"                    = "idx-cley-logistics"
    "DATABASE_URL"                          = "Server=tcp:${azurerm_mssql_server.sql.fully_qualified_domain_name},1433;Initial Catalog=${azurerm_mssql_database.db.name};"
    "OPENAI_API_KEY"                        = var.openai_api_key
    "SCK_ENVIRONMENT"                       = var.environment
  }
}

# 8. SEGURIDAD STAFF: Acceso de la Identidad de la App al SQL Server
# Esto permite que tu código Python entre al SQL sin usar el password de administrador
resource "azurerm_mssql_server_azuread_administrator" "sql_auth" {
  server_id           = azurerm_mssql_server.sql.id
  login_username      = azurerm_linux_function_app.app_engine.name
  object_id           = azurerm_linux_function_app.app_engine.identity[0].principal_id
  tenant_id           = azurerm_linux_function_app.app_engine.identity[0].tenant_id
  azuread_authentication_only = false # Permite ambos métodos por ahora
}