output "function_app_name" {
  value = azurerm_linux_function_app.app_engine.name
}

output "function_app_default_hostname" {
  description = "URL principal de la API del Asistente"
  value       = "https://${azurerm_linux_function_app.app_engine.default_hostname}"
}

output "sql_server_fqdn" {
  description = "Endpoint de la base de datos SQL"
  value       = azurerm_mssql_server.sql.fully_qualified_domain_name
}

output "app_insights_instrumentation_key" {
  value     = azurerm_application_insights.insights.instrumentation_key
  sensitive = true
}

output "search_service_endpoint" {
  value = "https://${azurerm_search_service.search.name}.search.windows.net"
}