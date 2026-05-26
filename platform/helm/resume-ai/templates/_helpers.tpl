{{- define "resume-ai.name" -}}
resume-ai
{{- end -}}

{{- define "resume-ai.labels" -}}
app.kubernetes.io/name: {{ include "resume-ai.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

