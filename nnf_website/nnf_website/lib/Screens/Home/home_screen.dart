import 'package:flutter/material.dart';
import 'package:nnf_website/Components/app_bar.dart';
import 'package:nnf_website/Components/dropzone_widget.dart';
class HomeScreen extends StatelessWidget {
  const HomeScreen({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
      // This size provide us total height and width of our screen
    Size size = MediaQuery.of(context).size;

    return Scaffold(
      body: Container(
        height: size.height,
        width: size.width,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage("assets/images/unsplash.jpg"),
            fit: BoxFit.cover,
            ),
        ),
        child: Stack(
          children: <Widget>[
            Stack(children: const [
              CustomAppBar(),
              DropzoneWidget(),
              ],
            )
            
          ],
        ),
      ),
    );

    
    
  }
}