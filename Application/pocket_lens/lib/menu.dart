import 'package:pocket_lens/ChangeIPAddress.dart';
import 'package:pocket_lens/alan_chatbot.dart';
import 'package:pocket_lens/barcode_reader.dart';
import 'package:pocket_lens/clothes_descriptor.dart';
import 'package:pocket_lens/emotion_recognizer.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'chatbot.dart';
import 'TTSTest.dart';
import 'scene_descriptor.dart';
import 'face_detector.dart';

class Menu extends StatelessWidget {
  String token = "";

  final String name;
  final String email;
  final String gender;

  Menu({
    required this.name,
    required this.email,
    required this.gender,
  });

  void _goToAlanChatbot(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return AlanChatBot();
        },
      ),
    );
  }

  void _goToChatbot(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return ChatBot();
        },
      ),
    );
  }

  void _goToBarcodeReader(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return BarcodeReader();
        },
      ),
    );
  }

  void _goToTTS(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return TTSTest();
        },
      ),
    );
  }

  void _goToSceneDescriptor(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const SceneDescriptor();
        },
      ),
    );
  }

  void _goToFaceDetector(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const FaceDetector();
        },
      ),
    );
  }

  void _goToChangeIPAddress(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return ChangeIPAddress();
        },
      ),
    );
  }

  void _goToEmotionRecognizer(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const EmotionRecognizer();
        },
      ),
    );
  }

  void _goToClothesDescriptor(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const ClothesDescriptor();
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(
              color: Color(0xFF106cb5),
              image: DecorationImage(
                fit: BoxFit.fill,
                image: AssetImage(
                  'assets/images/cover_image_sidebar.jpg',
                ), //Cover Image
              ),
            ),
            accountName: Text(
              name,
              style: const TextStyle(
                fontSize: 18,
              ),
            ),
            accountEmail: Text(
              email,
            ),
            currentAccountPicture: CircleAvatar(
              child: ClipOval(
                child: Image.asset(
                  'assets/images/user_icon.png',
                  fit: BoxFit.contain,
                ),
                // child: Image.network(
                //   userImage,
                //   fit: BoxFit.fill,
                // ),
              ),
            ),
          ),
          // /**********************/
          // const DrawerHeader(
          //   decoration: BoxDecoration(
          //     color: Colors.orangeAccent,
          //   ),
          //   child: Text('Profile'), // mmkn n7ot hena el usernaame
          // ),
          // /*******************************/
          ListTile(
            leading: const Icon(
              Icons.person,
              size: 27,
            ),
            title: const Text(
              'Profile',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              // _goToUserProfile(
              //   context,
              //   widget.name,
              //   widget.email,
              //   widget.phone,
              //   widget.gender,
              //   widget.carLicense,
              //   widget.carBrand,
              //   widget.carColour,
              // );
            },
          ),
          ListTile(
            onTap: () {
              _goToSceneDescriptor(context);
            },
            leading: const Icon(
              Icons.camera_alt_rounded,
              size: 27,
            ),
            title: const Text(
              'Scene Descriptor',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToFaceDetector(context);
            },
            leading: const Icon(
              Icons.face,
              size: 27,
            ),
            title: const Text(
              'Face Recognizer',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToEmotionRecognizer(context);
            },
            leading: const Icon(
              Icons.favorite,
              size: 27,
            ),
            title: const Text(
              'Emotion Recognizer',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToClothesDescriptor(context);
            },
            leading: const Icon(
              Icons.man,
              size: 27,
            ),
            title: const Text(
              'Clothes Descriptor',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToAlanChatbot(context);
            },
            leading: const Icon(
              Icons.message_rounded,
              size: 27,
            ),
            title: const Text(
              'Alan Chatbot',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToChatbot(context);
            },
            leading: const Icon(
              Icons.textsms_rounded,
              size: 27,
            ),
            title: const Text(
              'Chatbot',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.paid,
              size: 27,
            ),
            title: const Text(
              'Currency Detector',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToBarcodeReader(context);
            },
            leading: const Icon(
              Icons.barcode_reader,
              size: 27,
            ),
            title: const Text(
              'Barcode Reader',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.format_color_text_sharp,
              size: 27,
            ),
            title: const Text(
              'Text Reader',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),

          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.shopping_cart,
              size: 27,
            ),
            title: const Text(
              'Product Identifier',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.account_box,
              size: 27,
            ),
            title: const Text(
              'Call a contact',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.note_add,
              size: 27,
            ),
            title: const Text(
              'Note taker',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {},
            leading: const Icon(
              Icons.calendar_month,
              size: 27,
            ),
            title: const Text(
              'Event Scheduler',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            leading: const Icon(
              Icons.help,
              size: 27,
            ),
            title: const Text(
              'How it works',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              // _goToHowItWorks(context);
            },
          ),
          ListTile(
            leading: const Icon(
              Icons.settings,
              size: 27,
            ),
            title: const Text(
              'Settings',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              // _goToSettings(context, widget.token, widget.name);
            },
          ),
          ListTile(
            leading: const Icon(
              Icons.message,
              size: 27,
            ),
            title: const Text(
              'Contact Us',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              // _goContactUs(context);
            },
          ),
          ListTile(
            leading: const Icon(
              Icons.info,
              size: 27,
            ),
            title: const Text(
              'Change IP Address',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              _goToChangeIPAddress(context);
            },
          ),
          ListTile(
            leading: const Icon(
              Icons.logout,
              size: 27,
            ),
            title: const Text(
              'Logout',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              // _goToHome(context);
            },
          ),
          ListTile(
            leading: const Icon(
              Icons.exit_to_app,
              size: 27,
            ),
            title: const Text(
              'Exit',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              SystemNavigator.pop();
            },
          ),
          // ListTile(
          //   leading: const Icon(
          //     Icons.thermostat,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Text To Speech Widget (Test))',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          //   onTap: () {
          //     _goToTTS(context);
          //   },
          // ),
        ],
      ),
    );
  }
}
