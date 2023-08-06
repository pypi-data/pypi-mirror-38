
import requests, json, os
import struct, base64

from .SpeckleResource import SpeckleResource


class SpeckleApiClient():

	def ClientCreateAsync(self, client): 
		return

	def ClientDeleteAsync(self, client):
		return

	def ClientGetAllAsync():
		return

	def ClientGetAsync(self, client):
		return

	def ClientUpdateAsync(self, str, client):
		return

	def CommentCreateAsync(self, resourceType, str, comment):
		return

	def CommentDeleteAsync(self, str):
		return

	def CommentGetAsync(self, str):
		return

	def CommentGetFromResourceAsync(self, resourceType, str):
		return

	def CommentUpdateAsync(self, str, comment):
		return

	def GetObjectData(System.Runtime.Serialization.SerializationInfo, System.Runtime.Serialization.StreamingContext):
		return

	def JoinRoom(self, str):
		return

	def LeaveRoom(self, str):
		return

	def ObjectCreateAsync(self, objectList):
		return

	def ObjectDeleteAsync(self, objectId):
		return

	def ObjectGetAsync(self, objectId):
		return

	def ObjectGetBulkAsync(self, objectIdList, str):
		return

	def ObjectUpdateAsync(string, SpeckleCore.SpeckleObject, System.Threading.CancellationToken):
		return

	def ObjectUpdatePropertiesAsync(string, object, System.Threading.CancellationToken):
		return

	def PrepareRequest(System.Net.Http.HttpClient, System.Net.Http.HttpRequestMessage, System.Text.StringBuilder):
		return

	def ProcessResponse(System.Net.Http.HttpClient, System.Net.Http.HttpResponseMessage):
		return

	def ProjectCreateAsync(SpeckleCore.Project, System.Threading.CancellationToken):
		return

	def ProjectDeleteAsync(string, System.Threading.CancellationToken):
		return

	def ProjectGetAllAsync(System.Threading.CancellationToken):
		return

	def ProjectGetAsync(string, System.Threading.CancellationToken):
		return

	def ProjectUpdateAsync(string, SpeckleCore.Project, System.Threading.CancellationToken):
		return

	def StreamCloneAsync(string, System.Threading.CancellationToken):
		return

	def StreamCreateAsync(SpeckleCore.SpeckleStream, System.Threading.CancellationToken):
		return

	def StreamDeleteAsync(string, System.Threading.CancellationToken):
		return

	def StreamDiffAsync(string, string, System.Threading.CancellationToken):
		return

	def StreamGetAsync(string, string, System.Threading.CancellationToken):
		return

	def StreamGetObjectsAsync(string, string, System.Threading.CancellationToken):
		return

	def StreamsGetAllAsync(System.Threading.CancellationToken):
		return

	def StreamUpdateAsync(string, SpeckleCore.SpeckleStream, System.Threading.CancellationToken):
		return

	def UserGetAsync(System.Threading.CancellationToken):
		return

	def UserGetProfileByIdAsync(string, System.Threading.CancellationToken):
		return

	def UserLoginAsync(SpeckleCore.User, System.Threading.CancellationToken):
		return

	def UserRegisterAsync(SpeckleCore.User, System.Threading.CancellationToken):
		return

	def UserSearchAsync(SpeckleCore.User, System.Threading.CancellationToken):
		return

	def UserUpdateProfileAsync(SpeckleCore.User, System.Threading.CancellationToken):
		return
