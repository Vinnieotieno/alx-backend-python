from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    message = "Access denied. You must be a participant of this conversation."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "conversation"):
            participants = obj.conversation.participants.all()
        else:
            participants = obj.participants.all()

        if request.method in ["GET", "POST"]:
            return request.user in participants

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in participants

        return False
