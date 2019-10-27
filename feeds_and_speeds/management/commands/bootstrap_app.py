from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from feeds_and_speeds.models import ToolVendor, Tool, Machine, MaterialClass, Material, CuttingSpeeds, CuttingRecipe


class Command(BaseCommand):
    help = 'Bootstrap App'

    def handle(self, *args, **options):
        # Users
        superuser = User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin')

        # Tool Vendors
        tv_generic = ToolVendor.objects.create(name='Generic')
        tv_kobratec = ToolVendor.objects.create(name='Kobratec')

        # Tools
        t_kt_8mm = Tool.objects.create(
            vendor=tv_kobratec, name='8mm 3 Flute VHM Aluminum', flute_count=3, diameter=8, flute_length=19, fz_factor_at_one_ae=0.8, vc_factor_at_one_ae=0.75)
        t_kt_4mm = Tool.objects.create(
            vendor=tv_kobratec, name='4mm 3 Flute VHM Aluminum', flute_count=3, diameter=4, flute_length=8, fz_factor_at_one_ae=0.8, vc_factor_at_one_ae=0.75)
        t_gen_sm_50mm_alu = Tool.objects.create(
            vendor=tv_generic, name='50mm 4 Flute Insert Face Mill', flute_count=4, diameter=50, flute_length=3)

        # Machine
        machine = Machine.objects.create(
            name='Wabeco 1410 LF hs', spindle_power=2, max_rpm=7500, max_cutting_speed=600)

        # Material Classes
        mc_aluminum = MaterialClass.objects.create(name='Aluminum')

        # Materials
        m_almgsi = Material.objects.create(
            material_class=mc_aluminum, name='Al MgSi (6060)', kc_1_1=830, mc=0.23)

        # Cutting Speeds
        cs1 = CuttingSpeeds.objects.create(
            tool=t_gen_sm_50mm_alu, material=m_almgsi, feed_per_tooth=0.01, cutting_speed=230)
        cs2 = CuttingSpeeds.objects.create(
            tool=t_kt_8mm, material=m_almgsi, feed_per_tooth=0.02, cutting_speed=230)
        cs3 = CuttingSpeeds.objects.create(
            tool=t_kt_4mm, material=m_almgsi, feed_per_tooth=0.01, cutting_speed=230)

        # Cutting Recepies
        cr1 = CuttingRecipe.objects.create(cutter_data=cs1, ae=30, ap=1)
        cr2 = CuttingRecipe.objects.create(cutter_data=cs2, ae=0.8, ap=10)
        cr3 = CuttingRecipe.objects.create(cutter_data=cs3, ae=0.4, ap=5)
