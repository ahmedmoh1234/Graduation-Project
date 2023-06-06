import 'package:pocket_lens/ChangeIPAddress.dart';
import 'package:pocket_lens/alan_chatbot.dart';
import 'package:pocket_lens/barcode_reader.dart';
import 'package:pocket_lens/clothes_descriptor.dart';
import 'package:pocket_lens/contact-us.dart';
import 'package:pocket_lens/currency_recognizer.dart';
import 'package:pocket_lens/emotion_recognizer.dart';
import 'package:pocket_lens/product-identifier.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:pocket_lens/recommender.dart';
import 'package:pocket_lens/settings.dart';
import 'package:pocket_lens/test.dart';
import 'package:pocket_lens/text-reader.dart';
import 'package:pocket_lens/how_it_works.dart';
import 'package:pocket_lens/translate.dart';
import 'chatbot.dart';
import 'TTSTest.dart';
import 'scene_descriptor.dart';
import 'face_detector.dart';
import 'config.dart';

class Menu extends StatelessWidget {
  String token = "";
  final VoidCallback changeLanguage;

  final String name;
  final String email;
  final String gender;

  Menu({
    super.key,
    required this.name,
    required this.email,
    required this.gender,
    required this.changeLanguage,
  });

  void _goToCurrencyRecognizer(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const CurrencyRecognizer();
        },
      ),
    );
  }

  void _goToSettings(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return LanguageSettingsPage(
            changeLanguage: changeLanguage,
          );
        },
      ),
    );
  }

  void _goToHowItWorks(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return HowItWorks();
        },
      ),
    );
  }

  void _goToTranslate(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return Translate();
        },
      ),
    );
  }

  void _goContactUs(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return ContactUS();
        },
      ),
    );
  }

  void _goToTextReader(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const TextReader();
        },
      ),
    );
  }

  void _goToAlanChatbot(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const AlanChatBot();
        },
      ),
    );
  }

  void _goToChatbot(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const ChatBot();
        },
      ),
    );
  }

  void _goToProductIdentifier(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const ProductIdentifier();
        },
      ),
    );
  }

  void _goToBarcodeReader(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const BarcodeReader();
        },
      ),
    );
  }

  void _goToTTS(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const TTSTest();
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

  void _goToTest(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) {
          return const Test();
        },
      ),
    );
  }

  void _goToChangeIPAddress(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const ChangeIPAddress();
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

  void _goToRecommender(BuildContext ctx) {
    Navigator.of(ctx).push(
      MaterialPageRoute(
        builder: (_) {
          return const Recommender();
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
          // ListTile(
          //   leading: const Icon(
          //     Icons.person,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Profile',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          //   onTap: () {
          //     // _goToUserProfile(
          //     //   context,
          //     //   widget.name,
          //     //   widget.email,
          //     //   widget.phone,
          //     //   widget.gender,
          //     //   widget.carLicense,
          //     //   widget.carBrand,
          //     //   widget.carColour,
          //     // );
          //   },
          // ),
          ListTile(
            onTap: () {
              _goToSceneDescriptor(context);
            },
            leading: const Icon(
              Icons.camera_alt_rounded,
              size: 27,
            ),
            title: Text(
              useArabic ? 'واصف المشهد' : 'Scene Descriptor',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToSettings(context);
            },
            leading: const Icon(
              Icons.translate_rounded,
              size: 27,
            ),
            title: Text(
              useArabic ? 'اختيار اللغة' : 'Language',
              style: const TextStyle(
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
            title: Text(
              useArabic ? 'التعرف على الوجه' : 'Face Recognizer',
              style: const TextStyle(
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
            title: Text(
              useArabic ? 'التعرف على المشاعر' : 'Emotion Recognizer',
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
            title: Text(
              useArabic ? 'التعرف على الملابس' : 'Clothes Descriptor',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToRecommender(context);
            },
            leading: const Icon(
              Icons.recommend_outlined,
              // color: Colors.green,
              size: 27,
            ),
            title: Text(
              useArabic ? 'اقتراح الملابس' : 'Recommender',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          // ListTile(
          //   onTap: () {
          //     _goToAlanChatbot(context);
          //   },
          //   leading: const Icon(
          //     Icons.textsms_rounded,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Chatbot',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          // ),
          ListTile(
            onTap: () {
              _goToChatbot(context);
            },
            leading: const Icon(
              Icons.textsms_rounded,
              size: 27,
            ),
            title: Text(
              useArabic ? 'شات بوت' : 'Face Recognizer',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          ListTile(
            onTap: () {
              _goToCurrencyRecognizer(context);
            },
            leading: const Icon(
              Icons.paid,
              size: 27,
            ),
            title: Text(
              useArabic ? 'التعرف على النقود' : 'Currency Recognizer',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),

          ListTile(
            onTap: () {
              _goToTextReader(context);
            },
            leading: const Icon(
              Icons.format_color_text_sharp,
              size: 27,
            ),
            title: Text(
              useArabic ? 'قراءة النص' : 'Text Reader',
              style: TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),

          ListTile(
            onTap: () {
              _goToProductIdentifier(context);
            },
            leading: const Icon(
              Icons.shopping_cart,
              size: 27,
            ),
            title: Text(
              useArabic ? 'التعرف على المنتجات' : 'Product Identifier',
              style: const TextStyle(
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
            title: Text(
              useArabic ? 'قراءة الباركود' : 'Barcode Reader',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
          ),
          // ListTile(
          //   onTap: () {},
          //   leading: const Icon(
          //     Icons.account_box,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Call a contact',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          // ),

          // ListTile(
          //   onTap: () {},
          //   leading: const Icon(
          //     Icons.note_add,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Note taker',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          // ),
          // ListTile(
          //   onTap: () {},
          //   leading: const Icon(
          //     Icons.calendar_month,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Event Scheduler',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          // ),
          ListTile(
            leading: const Icon(
              Icons.help,
              size: 27,
            ),
            title: Text(
              useArabic ? 'كيف يعمل' : 'How It Works',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              _goToHowItWorks(context);
            },
          ),
          // ListTile(
          //   leading: const Icon(
          //     Icons.settings,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Settings',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          //   onTap: () {
          //     _goToSettings(context);
          //   },
          // ),
          ListTile(
            leading: const Icon(
              Icons.message,
              size: 27,
            ),
            title: Text(
              useArabic ? 'تواصل معنا' : 'Contact Us',
              style: const TextStyle(
                fontSize: 17,
                fontFamily: 'RalewayMedium',
              ),
            ),
            onTap: () {
              _goContactUs(context);
            },
          ),
          // ListTile(
          //   leading: const Icon(
          //     Icons.info,
          //     size: 27,
          //   ),
          //   title: const Text(
          //     'Change IP Address',
          //     style: TextStyle(
          //       fontSize: 17,
          //       fontFamily: 'RalewayMedium',
          //     ),
          //   ),
          //   onTap: () {
          //     _goToChangeIPAddress(context);
          //   },
          // ),
          ListTile(
            leading: const Icon(
              Icons.logout,
              size: 27,
            ),
            title: Text(
              useArabic ? 'تسجيل خروج' : 'Logout',
              style: const TextStyle(
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
            title: Text(
              useArabic ? 'خروج من التطبيق' : 'Exit',
              style: const TextStyle(
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
