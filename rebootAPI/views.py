from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from machinerequests.models import CPU, OperatingSystem, Preset, Request, Machine
from django.contrib.auth.models import User

# Data Serializers


class CPUSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CPU
        fields = ('name', 'cores', 'x64', 'clock')


class OperatingSystemSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ('name', 'version', 'experimental')


class PresetSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preset
        fields = ('cpu', 'ram', 'hhd')


class RequestSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = ('family_name', 'given_name', 'requester_type', 'faculty_and_dept', 'organization', 'preset', 'os',
            'machine_use', 'need_display', 'need_keyboard', 'need_mouse', 'need_ethernet', 'extra_information',
            'amount', 'filled', 'filled_at', 'requested_at')


class MachineSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ('request', 'fulfiller', 'cpu', 'ram', 'hdd', 'pickedup_at', 'notes', 'picked_up')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'is_staff')

# View Sets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer


class OperatingSystemViewSet(viewsets.ModelViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer


class PresetViewSet(viewsets.ModelViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class PendingMachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.filter(picked_up=False)
    serializer_class = MachineSerializer


class PendingRequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.filter(filled=False)
    serializer_class = RequestSerializer

# The router routes all the routes

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cpus', CPUViewSet)
router.register(r'os', OperatingSystemViewSet)
router.register(r'presets', PresetViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'machines', MachineViewSet)
router.register(r'machines/pending', PendingMachineViewSet)
router.register(r'requests/pending', PendingRequestViewSet)


def get_router():
    return router