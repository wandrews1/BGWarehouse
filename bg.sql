-- DROP DATABASE IF EXISTS bg;
CREATE DATABASE  bg;

\c bg;

-- GRANT SELECT, INSERT ON DATABASE bg TO bgtemp;

CREATE EXTENSION pgcrypto;

-- CREATE USER bgtemp with login;

DROP TABLE IF EXISTS login;
CREATE TABLE login (
  email varchar(50) NOT NULL,
  fname text NOT NULL,
  lname text  NOT NULL,
  pw1 text NOT NULL,
  address text NOT NULL,
  city text NOT NULL,
  state text NOT NULL,
  zipcode varchar(5) NOT NULL,
  userLevel text NOT NULL
  );

INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('bkertche@umw.edu','Brendon', 'Kertcher', crypt('pass', gen_salt('bf')), 'Somewhere', 'Fredericksburg', 'VA', '22407','Administrator');
INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('scripture187@gmail.com','Billy', 'Andrews', crypt('pass', gen_salt('bf')), '78 C L Walker Blvd', 'Fredericksburg', 'VA', '22407','Administrator');
INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('jhuffma3@umw.edu','Jacob', 'Huffman', crypt('pass', gen_salt('bf')), 'Somewhere', 'Fredericksburg', 'VA', '22407','Administrator');
INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('manager@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), 'test', 'test', 'VA', '22407','Manager');
INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('sales@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), 'test', 'test', 'VA', '22407','Sales Associate');
INSERT INTO login (email, fname, lname, pw1, address, city, state, zipcode, userLevel) VALUES ('customer@umw.edu','Test', 'test', crypt('pass', gen_salt('bf')), 'test', 'test', 'VA', '22407','Customer');
GRANT SELECT, INSERT ON login TO bgtemp;



DROP TABLE IF EXISTS items;
CREATE TABLE items (
  productID varchar NOT NULL,
  cost float NOT NULL,
  quantity int NOT NULL,
  category text NOT NULL,
  name varchar NOT NULL,
  description varchar NOT NULL
  );
-- use two " '' " to use an apostrophe, like 'McCoy''s BBQ'
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (485, 3.99, 150, 'Battery', 'Battery Cleaner - Acid Detector', 'BG Battery Cleaner – Acid Detector removes corrosion from battery terminals, cables and carriers. It also turns red to warn of the presence of acid or a crack or leak around terminal.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (985, 3.99, 150, 'Battery', 'Battery Terminal Protectors', 'BG Battery Terminal Protectors protect battery terminals from corrosive buildup. The chemical formula is harmless to the battery, paint and other parts.  Fits easily onto the battery posts.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (490, 3.99, 150, 'Battery', 'Ignition & Battery Terminal Sealer', 'BG Ignition & Battery Terminal Sealer completely seals and weatherproofs wiring and electrical connections.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (885, 3.99, 150, 'Battery', 'Battery Cleaner & Leak Detector', 'BG Battery Cleaner & Leak Detector removes corrosion from battery terminals, cables and carriers. It also turn reds to warn of the presence of acid or a crack or leak around terminal.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (979, 3.99, 150, 'Battery', 'Battery Cable Savers', 'BG Battery Cable Savers correct this problem by filling in the extra space, allowing the cable to be tightened to complete a solid connection. A solid connection eliminates the starting problems that the faulty connection causes.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (841, 3.99, 150, 'Brakes', 'Low Viscosity DOT 4 Brake Fluid', 'BG Low Viscosity DOT 4 Brake Fluid delivers quick brake response at low temperatures for all DOT 4 disc and drum brake systems. ');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (840, 3.99, 150, 'Brakes', 'DOT 4 Brake Fluid', 'BG DOT 4 Brake Fluid provides the ultimate high temperature protection and moisture resistance for all DOT 4 disc and drum brake systems. Brake systems can produce pressure up to 2000 psi. This pressure, along with extreme heat from the friction of braking, cause brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (835, 3.99, 150, 'Brakes', 'Super DOT 4 Brake Fluid', 'BG Super DOT 4 Brake Fluid provides the ultimate high temperature protection and high boiling point protection above and beyond regular DOT 4 fluid. Brake systems can produce pressure up to 2000 psi! This pressure – along with extreme heat from the friction of braking – causes brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (850, 3.99, 150, 'Brakes', 'DOT 3 Brake Fluid', 'BG DOT 3 Brake Fluid provides the ultimate high temperature protection and moisture resistance for all DOT 3 disc and drum brake systems. Brake systems can produce pressure up to 2000 psi. This pressure, along with extreme heat from the friction of braking, cause brake fluid to break down. This compromised brake fluid will boil at a lower temperature leaving air pockets and condensation in the brake system. Water in the brake system causes a myriad of problems such as brake deposits and varnish buildup.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('FES400', 3.99, 150, 'Brakes', 'Xpress Brake System Fluid Exchange System', 'BG Xpress Brake System Fluid Exchange System is a small machine that quickly and effectively removes oxidized and corrosive brake fluid, replacing it with new fluid. The exchange is performed in minutes. Brakes work by creating friction to slow and stop a vehicle. This friction creates a substantial amount of heat which in turn causes rapid oxidation of brake fluid. Deposits form in the brake system causing serious brake system malfunction which compromises the vehicle’s safety.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('PF7', 3.99, 150, 'Brakes', 'PF7 Brake Service System', 'Brake Service System quickly and effectively removes oxidized and corrosive brake fluid, replacing it with new fluid. The exchange is performed in minutes in a contained unit. No hassle. No mess.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (402, 3.99, 150, 'Brakes', '402 Brake & Contact Cleaner', 'BG 402 Brake & Contact Cleaner is a quick and efficient brake cleaner that dissolves built up residue on brake components. Residue on brake components leads to obnoxious brake squeal and chatter. Brake systems are sensitive to the buildup of brake fluid, grease, oil, moisture, and other residue that can form on drum and disc assemblies. ');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (403, 3.99, 150, 'Brakes', '403 Non-Chlorinated Brake Cleaner', 'Like BG 402, BG 403 Non-Chlorinated Brake Cleaner is a quick and efficient brake cleaner that dissolves built up residue on brake components, but without chlorinated solvents.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (860, 3.99, 150, 'Brakes', 'Stop Squeal', 'BG Stop Squeal eliminates annoying, whining, or squealing brakes.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('605BK', 3.99, 150, 'Brakes', 'Brake Lube', 'BG Brake Lube is a professional-use brake grease. BG Brake Lube is applied to the caliper bracket that holds the brake pad in place. This allows pads to slide and contact the brake rotor as they wear down. Without BG Brake Lube on these caliper brackets, the brake pad may not slide inward correctly, which can cause brake pads to wear unevenly. BG Brake Lube performs exceptionally well in all applications and under all conditions. It mixes with virtually any soap-based grease with excellent seal compatibility.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (709, 3.99, 150, 'Climate', 'Frigi-Clean', 'BG Frigi-Clean removes accumulated bacteria, mold, spores, road grime, nicotine oil, and debris and restores heating/cooling efficiency.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (702, 3.99, 150, 'Climate', 'Universal Frigi-Quiet for R-1234yf', 'BG Universal Frigi-Quiet for R-1234yf enhances cooling, ensures quieter compressor operation and prolongs compressor life.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (701, 3.99, 150, 'Climate', 'Universal Frigi-Quiet for R-134a', 'BG Universal Frigi-Quiet for R-134a enhances cooling, ensures quieter compressor operation and prolongs compressor life.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (704, 3.99, 150, 'Climate', 'Universal Frigi-Charge', 'BG Universal Frigi-Charge extends compressor life and provides overall quieter and cooler running A/C systems.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (708, 3.99, 150, 'Climate', 'Frigi-Fresh', 'BG Frigi-Fresh will safely and effectively eliminate foul, musty odors from A/C systems.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (917-2, 3.99, 150, 'Climate', 'Mechanical Additive Injector Tool', 'The BG Mechanical Additive Injector Tool is the perfect choice for manually adding BG Universal Frigi-Quiet to a charged air conditioning system. This quick and easy, professional-use tool is designed for use without charging stations or manifold gauge sets.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (546, 3.99, 150, 'Cooling', 'Universal Super Cool', 'BG Universal Super Cool protects against foaming and corrosion and restores critical coolant additive balance and coolant pH.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (540, 3.99, 150, 'Cooling', 'Universal Cooling System Cleaner', 'BG Universal Cooling System Cleaner removes built-up scale, oil, and harsh mineral deposits. It also removes tough residues caused by oil fouling and coolant inhibitor breakdown.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (511, 3.99, 150, 'Cooling', 'Universal Cooling System Sealer', 'BG Universal Cooling System Sealer quickly and completely plugs leak points in the coolant system. Refined organic fibers carry sealer particles that build on each other around a hole until it is completely plugged.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('FES200', 3.99, 150, 'Cooling', 'Xpress Cooling System Fluid Exchange System', 'BG Xpress Cooling System Fluid Exchange System is a small machine that quickly and efficiently installs new coolant while simultaneously removing worn out coolant.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('CT2', 3.99, 150, 'Cooling', 'CT2 Coolant Transfusion System', 'BG CT2 Coolant Transfusion System quickly and efficiently installs new 50/50 coolant while simultaneously removing worn out coolant.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (589, 3.99, 150, 'Cooling', 'Universal Coolant/Antifreeze', 'BG Universal Coolant/Antifreeze offers complete and long-lasting cooling system protection under the most severe conditions. It is designed to be used in all gasoline, diesel, and compressed natural gas fueled engines.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('CT4', 3.99, 150, 'Cooling', 'CT4 Coolant Transfusion System', 'BG CT4 Coolant Transfusion System uses a vacuum to remove worn out coolant from the cooling system and then installs new 50/50 coolant back into the system with no air pockets.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES ('CT6', 3.99, 150, 'Cooling', 'CT6 Large Capacity Coolant Transfusion System', 'BG CT6 Large Capacity Coolant Transfusion System vacuums out used coolant and then installs new coolant.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (587, 3.99, 150, 'Cooling', 'AB Complete', 'BG AB Complete rejuvenates worn out coolant, giving it back its corrosion prevention abilities.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (245, 3.99, 150, 'Diesel', '245 Premium Diesel Fuel System Cleaner', 'BG 245 Premium Diesel Fuel System Cleaner removes and dissolves deposits from the entire diesel injection system, including fuel injectors and combustion chambers.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (244, 3.99, 150, 'Diesel', '244', 'BG 244 is a powerhouse diesel fuel system cleaner. BG 244 is like BG 44K for diesels.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (229, 3.99, 150, 'Diesel', 'Diesel Care', 'BG Diesel Care is a highly effective diesel fuel injection system cleaner.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (9700-550, 3.99, 150, 'Diesel', 'Diesel VIA', 'BG Diesel VIA is the ultimate diesel injector cleaning system for passenger cars, SUVs and light trucks.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (227, 3.99, 150, 'Diesel', 'DFC with Lubricity', 'BG DFC with Lubricity is a superior multi-functional diesel fuel conditioner.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (230, 3.99, 150, 'Diesel', 'DFC Plus', 'BG DFC Plus is a professional-use diesel conditioner that guards fuel system components against corrosion, corrects nozzle buildup, and keeps the fuel system clean.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (247, 3.99, 150, 'Diesel', 'DFC Plus Easy Treat', 'BG DFC Plus Easy Treat contains all the benefits of BG DFC Plus concentrated in a conveniently-sized bottle for individual truck tanks.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (248, 3.99, 150, 'Diesel', 'DFC Plus with Cetane Improver', 'BG DFC Plus with Cetane Improver protects fuel system components from corrosion and deposits, prevents fuel gelling, and reduces exhaust smoke. It is a professional use diesel conditioner containing a lubricity agent that protects against the effects of low-sulfur diesel and a cetane improver that raises the diesel cetane rating by 3-7 values.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (225, 3.99, 150, 'Diesel', 'DFC with Lubricity HP', 'BG DFC with Lubricity HP is a diesel fuel conditioner plus lubricity for high pressure common rail diesels.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (232, 3.99, 150, 'Diesel', 'DFC Plus HP', 'BG DFC Plus HP for high pressure common rail diesel engines provides excellent fuel system protection for the high temperatures and pressures of high pressure diesel systems.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (237, 3.99, 150, 'Diesel', 'DFC Plus HP Extra Cold Weather Performance', 'BG DFC Plus HP Extra Cold Weather Performance cleans fuel injector deposits and prevents black fuel filter plugging in High Pressure Common Rail (HPCR) systems.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (240, 3.99, 150, 'Diesel', 'DFC Plus for Biodiesel', 'BG DFC Plus for Biodiesel conditions biodiesel, cleans fuel systems, and helps to prevent fuel deposits. It’s safe for both common rail and direct injection fuel engines.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (256, 3.99, 150, 'Diesel', 'Diesel Thaw', 'BG Diesel Thaw quickly and efficiently liquefies gelled diesel fuel and melts ice crystals, restoring fuel flow.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (255, 3.99, 150, 'Diesel', 'Diesel ISC Induction System Cleaner', 'BG Diesel ISC Induction System Cleaner powers through oil deposits and unburned fuel left behind by exhaust system.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (9255-550, 3.99, 150, 'Diesel', 'Diesel Induction Service Set', 'As part of the Diesel Induction Service, the BG Diesel Induction Service Set sends BG Diesel ISC Induction System Cleaner through the EGR runners and the fresh air intake.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (2581, 3.99, 150, 'Diesel', 'DPF & Emissions System Restoration', 'BG DPF & Emissions System Restoration safely dissolves and removes hydrocarbon deposits, especially soot, from the air intake and emissions system. Used by a professional with the BG 12Q VIA, PN 9300, this product restores fuel economy, reduces emissions and prolongs component life. ');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (9300, 3.99, 150, 'Diesel', '12Q VIA', 'BG 12Q VIA, PN 9300, is a one-of-a-kind diesel intake and emissions system cleaning machine that allows technicians to not only command Diesel Particulate Filter (DPF) regeneration, but to control it for a thorough cleaning. ');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (233, 3.99, 150, 'Diesel', 'Diesel Fuel De-icer', 'BG Diesel Fuel De-icer is specially formulated to protect wet, high cloud point diesel fuel from icing.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (215, 3.99, 150, 'Diesel', 'Diesel Fuel Pour Depressant', 'BG Diesel Fuel Pour Depressant improves fuel pumpability in cold weather conditions without altering other diesel fuel properties.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (228, 3.99, 150, 'Diesel', 'Diesel Fuel Cetane Improver', 'BG Diesel Cetane Improver increases the cetane number of diesel fuel. For a diesel fuel conditioner with added cetane improver, check out BG DFC Plus with Cetane Improver.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (224, 3.99, 150, 'Diesel', 'Diesel Pump Lubricant', 'BG Diesel Pump Lubricant provides the needed lubricity to that prevents low-sulfur diesel fuels from scuffing and scoring on the surfaces of fuel injection pump.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (751, 3.99, 150, 'DriveLine', 'Ultra-Guard LS Full Synthetic Gear Lubricant', 'BG Ultra-Guard LS Full Synthetic Gear Lubricant provides the ultimate in simplicity and ease when servicing for drive line components, especially those requiring limited slip function.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (753, 3.99, 150, 'DriveLine', 'Ultra-Guard LS Heavy Duty', 'BG Ultra-Guard LS Heavy Duty provides the ultimate in simplicity and ease when servicing for drive line components, especially those requiring limited slip function.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (792, 3.99, 150, 'DriveLine', 'Syncro Shift II', 'BG Syncro ShiftII is a specially formulated gear lubricant designed for front wheel drive manual transmissions. It reduces maintenance costs by improving thermal stability, low-temperature fluidity, and shear stability while providing smoother shifting and improved seal compatibility.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (939, 3.99, 150, 'DriveLine', 'Drive Line Service Center', 'The BG Drive Line Service Center provides a fast, easy, and clean way of servicing all types of automotive differentials, manual transmissions, manual transaxles and transfer cases in light- and heavy-duty vehicles.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (752, 3.99, 150, 'DriveLine', 'Ultra Guard Heavy Duty', 'BG Ultra-Guard Heavy Duty provides the ultimate protection for drive line components. Specifically designed for heavy duty and commercial vehicles, it has superior thermal stability, smoother gear shifting, optimum drive line efficiency, quieter operation, protection against wear, pitting, and corrosion, seal compatibility and improved seal performance.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (750, 3.99, 150, 'DriveLine', 'Ultra-Guard Full Synthetic Gear Lubricant', 'BG Ultra-Guard is a revolutionary multi-purpose synthetic gear oil compatible with all car and truck applications calling for GL-5 gear oil. It provides superior thermal stability, smoother gear shifting, optimum drive line efficiency, quieter operation, protection against wear, pitting, and corrosion, seal compatibility and improved seal performance.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (328, 3.99, 150, 'DriveLine', 'Universal MGC', 'BG Universal MGC is designed to protect both conventional and limited slip differentials. It enhances lubricant film thickness and improves extreme pressure characteristics of any gear oil.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (325, 3.99, 150, 'DriveLine', 'MGC Multi-Gear Concentrate', 'BG MGC is an innovative professional-use gear oil additive that enhances film thickness and strength, improves thermal stability and lubricant life, and smooths manual transmission shifting characteristics. It will reduce component wear, gear box temperature, and limited slip differential chatter.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', 'BG MOA is the number one engine oil supplement! In a recent survey, dealership service managers chose BG MOA 8 to 1 over the next aftermarket supplier.');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');
INSERT INTO items (productID, cost, quantity, category, name, description) VALUES (110, 3.99, 150, 'Engine', 'MOA', '');






GRANT SELECT, INSERT ON items TO bgtemp;



DROP TABLE IF EXISTS messages;
CREATE TABLE messages (
  fname text NOT NULL,
  lname text NOT NULL,
  message text NOT NULL,
  time timestamptz NOT NULL DEFAULT now()
  );

INSERT INTO messages (fname, lname, message) VALUES ('FaceBot','', 'Booting System...');
INSERT INTO messages (fname, lname, message) VALUES ('FaceBot','', 'FaceChat now LIVE!');

GRANT SELECT, INSERT ON messages TO bgtemp;

